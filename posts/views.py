from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from posts.models import Post

# Create your views here.


def post_create(request):
    context = {
        'title': 'create'
    }
    return render(request, 'index.html', context)


def post_detail(request, id):
    instance = get_object_or_404(Post, id = id)
    context = {
        'title': 'detail',
        'instance': instance
    }
    return render(request, 'post_detail.html', context)


def post_list(request):
    queryset = Post.objects.all()
    if request.user.is_authenticated():
        context = {
            'title': 'my user list',
            'object_list': queryset
        }
    else:
        context = {
            'title': 'list'
        }
    return render(request, 'index.html', context)
    #return HttpResponse('<h1>Hello to Posts</h1>')


def post_update(request):
    context = {
        'title': 'update'
    }
    return render(request, 'index.html', context)


def post_delete(request):
    context = {
        'title': 'delete'
    }
    return render(request, 'index.html', context)
