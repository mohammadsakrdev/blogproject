from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import (ModelSerializer, ValidationError, SerializerMethodField)
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from ..models import Comment


User = get_user_model()


def create_comment_serializer(model_type='post', id=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp'
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.id = id
            self.parent_obj = None
            self.user = user
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError('this is not a valid content type')
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=self.id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError('this is not a valid id for this model')
            return data

        def create(self, validated_data):
            content = validated_data.get('content')
            if self.user:
                user = self.user
            else:
                user = User.objects.all().first()
            model_type = self.model_type
            id = self.id
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type=model_type,
                id=id,
                user=user,
                content=content,
                parent_obj=parent_obj)
            return comment

    return CommentCreateSerializer


class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
        ]


class CommentDetailSerializer(ModelSerializer):
    content_object_url = SerializerMethodField()
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'content_object_url',
            'content',
            'timestamp',
            'reply_count',
            'replies',
        ]

        read_only_fields=[
            'id',
            'content_type',
            'content_object_url',
            'timestamp',
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        return obj.content_object.get_api_url()

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentListSerializer(ModelSerializer):
    reply_count = SerializerMethodField()

    url = HyperlinkedIdentityField(
        view_name='comments-api:detail',
        lookup_field='id'
        )

    class Meta:
        model = Comment
        fields = [
            'id',
            'url',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0