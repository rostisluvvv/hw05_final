from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm
from django.conf import settings


def pagination(request, post_list):
    paginator = Paginator(post_list, settings.COUNT_POSTS)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    post_list = Post.objects.all()
    page_obj = pagination(request, post_list)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = pagination(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    count_posts = post_list.count()
    page_obj = pagination(request, post_list)

    following = request.user.is_authenticated and author.following.filter(
        user=request.user
    ).exists()

    context = {
        'username': username,
        'author': author,
        'page_obj': page_obj,
        'count_posts': count_posts,
        'following': following

    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    posts_detail = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm(request.POST or None)
    comments = posts_detail.comments.all()
    context = {
        'posts_detail': posts_detail,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    template_name = 'posts/create_post.html'
    context = {'form': form}
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('posts:profile', request.user)
    return render(request, template_name, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if request.user != post.author:
        return redirect('posts:post_detail', post.id)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.id)

    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    template_name = 'posts/create_post.html'
    return render(request, template_name, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    authors = Follow.objects.filter(user=request.user).values_list('author',
                                                                   flat=True)
    post_list = Post.objects.filter(author__in=authors)
    page_obj = pagination(request, post_list)
    context = {'page_obj': page_obj}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    is_subscribed, follow_obj = Follow.objects.get_or_create(
        user=request.user, author=author
    )
    if request.user != author and not is_subscribed:
        follow_obj.create()
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follow_filter = Follow.objects.filter(user=request.user, author=author)
    is_subscribed = follow_filter
    if request.user != author and is_subscribed:
        follow_filter.delete()
    return redirect('posts:profile', username=username)
