from rest_framework.generics import (ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import (IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.filters import (SearchFilter, OrderingFilter)
from posts.models import Post
from .serializers import (PostDetailSerializer, PostListSerializer, PostCreateSerializer)
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination)
from .pagination import PostLimitOffsetPagination


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    lookup_field = 'id'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'user__first_name']
    pagination_class = PostLimitOffsetPagination #LimitOffsetPagination PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView,self).get_queryset(*args, **kwargs)
        queryset_list = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'id'


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'id'


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
