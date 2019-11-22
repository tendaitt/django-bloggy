from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import get_object_or_404, render, redirect

from blog.models import Post
from blog.forms import PostForm

# helper function
def encode_url(url):
    return url.replace(' ', '_')

def get_popular_posts():
    popular_posts = Post.objects.order_by('-views')[:5]
    for popular_post in popular_posts:
        popular_post.url = encode_url(popular_post.title)
    return popular_posts

def index(request):
    latest_posts = Post.objects.all().order_by('-created_at')
    popular_posts = get_popular_posts()
    t = loader.get_template('blog/index.html')
    c = {'latest_posts': latest_posts, 'popular_posts': popular_posts}
    for post in latest_posts:
        post.url = encode_url(post.title)
    return HttpResponse(t.render(c))

def post(request, post_url):
    single_post = get_object_or_404(Post, title=post_url.replace('_', ' '))
    popular_posts = get_popular_posts()
    single_post.views += 1
    single_post.save()
    t = loader.get_template('blog/post.html')
    c = {'single_post': single_post, 'popular_posts': popular_posts}
    return HttpResponse(t.render(c))

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect(index)
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})