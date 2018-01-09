from rest_framework.serializers import (ModelSerializer, HyperlinkedIdentityField, SerializerMethodField)
from ..models import Post
from comments.api.serializers import CommentSerializer
from comments.models import Comment


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='id'
    )

    user = SerializerMethodField()

    delete_url = HyperlinkedIdentityField(
        view_name='posts-api:delete',
        lookup_field='id'
    )

    def get_user(self, obj):
        return str(obj.user.username)

    class Meta:
        model = Post
        fields = [
            'title',
            'id',
            'user',
            'content',
            'publish',
             'url',
            'delete_url',
        ]


class PostDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    image = SerializerMethodField()
    markdown = SerializerMethodField()
    comments = SerializerMethodField()

    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments

    def get_markdown(self, obj):
        return obj.get_markdown()

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    class Meta:
        model = Post
        fields = [
            'title',
            'user',
            'image',
            'id',
            'content',
            'publish',
            'markdown',
            'comments'
        ]


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
            'user',
        ]