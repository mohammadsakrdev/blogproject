from rest_framework.generics import (ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import (IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.filters import (SearchFilter, OrderingFilter)
from rest_framework.mixins import (DestroyModelMixin, UpdateModelMixin)
from django.db.models import Q
from .serializers import (CommentSerializer, create_comment_serializer, CommentDetailSerializer, CommentListSerializer)

from posts.api.pagination import PostLimitOffsetPagination
from posts.api.permissions import IsOwnerOrReadOnly

from comments.models import Comment


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    lookup_field = 'id'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostLimitOffsetPagination #LimitOffsetPagination PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView,self).get_queryset(*args, **kwargs)
        queryset_list = Comment.objects.filter(id__gte=0)
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list


class CommentEditAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = 'id'


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    #serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    #def perform_create(self, serializer):
     #   serializer.save(user=self.request.user)

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        id = self.request.GET.get('id')
        parent_id = self.request.GET.get('parent_id', None)

        return create_comment_serializer(model_type=model_type,
                                         id=id, parent_id=parent_id,
                                         user=self.request.user)


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=1)
    serializer_class = CommentDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'


class CommentUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
