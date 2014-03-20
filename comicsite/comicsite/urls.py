from django.conf.urls import patterns, include, url
from django.contrib import admin
from comicLibrary import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comicsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^comicLibrary/', include('comicLibrary.urls')),
    url(r'^comicLibrary/\d+/media/(?P<comic_id>\d+)$',views.comic_download, name='comic_download'),
    url(r'^admin/', include(admin.site.urls)),
)
