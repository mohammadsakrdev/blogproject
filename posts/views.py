
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q

from urllib.parse import quote

from posts.forms import PostForm
from posts.models import Post

from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise  Http404
    #if not request.user.is_authenticated():
    #    raise  Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'Created Successfully')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form,
        'title': 'Create Post'
    }
    return render(request, 'post_form.html', context)


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    if instance.draft or instance.publish > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote(instance.content)
    comments = instance.comments #Comment.objects.filter_by_instance(instance)
    initial_data = {
        'content_type': instance.get_content_type,
        'object_id': instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        object_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        'title': 'detail',
        'instance': instance,
        'share_string':share_string,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'post_detail.html', context)


def post_list(request):
    queryset_list = Post.objects.active()#all().order_by('-timestamp')
    today = timezone.now().date()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 10) # Show 25 Posts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    if request.user.is_authenticated():
        context = {
            'title': 'Posts List',
            'object_list': queryset,
            'page_request_var': page_request_var,
            'today':today
        }
    else:
        context = {
            'title': 'Posts List'
        }
    return render(request, 'post_list.html', context)


def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise  Http404
    instance = get_object_or_404(Post, id = id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Updated Successfully')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': 'update',
        'instance': instance,
        'form': form
    }
    return render(request, 'post_form.html', context)


def post_delete(request, id=None):
    if not request.user.is_staff or request.user.is_superuser:
        raise  Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Deleted Successfully')
    return redirect('posts:list')
