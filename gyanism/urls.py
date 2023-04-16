"""gyanism URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from blog.views import index, about, post, contact, search, profile
from django.conf.urls import url
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap,StaticSitemap

sitemaps={
    'post':PostSitemap,
    'static':StaticSitemap,
    }

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = 'home'),
    path('about/', about, name = 'about'),
    path('post/<int:id>/<slug:slug>', post, name = 'post'),
    path('contact/', contact, name = 'contact'),
    path('search/', search, name = 'search'),
    path('profile/', profile, name='profile'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
    path(
        "ads.txt",
        RedirectView.as_view(url=staticfiles_storage.url("ads.txt")),
    ),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps}),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
#urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Gyanism"
admin.site.site_title = "Admin Area | Gyanism"
admin.site.index_title = "GOD Mode | Gyanism"
