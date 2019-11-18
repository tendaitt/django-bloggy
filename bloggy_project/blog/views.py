from django.http import HttpResponse
from django.template import Context, loader

from blog.models import Post

def index(request):
    latest_posts = Post.objects.all().order_by('-created_at')
    t = loader.get_template('blog/index.html')
    c = {'latest_posts': latest_posts, }
    return HttpResponse(t.render(c))