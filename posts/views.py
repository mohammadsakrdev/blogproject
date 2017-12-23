from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from posts.forms import PostForm
from posts.models import Post

# Create your views here.


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

    context = {
        'form': form,
        'title': 'Create Post'
    }
    return render(request, 'post_form.html', context)


def post_detail(request, id=None):
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


def post_update(request, id=None):
    instance = get_object_or_404(Post, id = id)
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {
        'title': 'update',
        'instance': instance,
        'form': form
    }
    return render(request, 'post_form.html', context)


def post_delete(request):
    context = {
        'title': 'delete'
    }
    return render(request, 'index.html', context)
