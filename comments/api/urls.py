
from django.conf.urls import url
from .views import (CommentDetailAPIView, CommentListAPIView, CommentCreateAPIView, CommentEditAPIView)

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^(?P<id>\d+)/$', CommentDetailAPIView.as_view(), name='detail'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name='create'),
    #url(r'^(?P<id>\d+)/edit/$', CommentEditAPIView.as_view(), name='edit'),
    ]