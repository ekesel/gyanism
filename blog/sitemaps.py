from django.contrib.sitemaps import  Sitemap
from .models import Post
from django.urls import reverse

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.time_upload
        
    def location(self,obj):
        return "/post/{0}/{1}".format(obj.id,obj.slug)


class StaticSitemap(Sitemap):
    changefreq = "never"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return ['home', 'contact','about']

    def location(self, item):
        return reverse(item)
