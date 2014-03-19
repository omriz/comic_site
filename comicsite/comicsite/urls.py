from django.conf.urls import patterns, include, url
from django.contrib import admin
from comicLibrary import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comicsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^comicLibrary/', include('comicLibrary.urls')),
    url(r'^(?P<series_id>\d+)/$', views.detail, name='detail'),
    url(r'^admin/', include(admin.site.urls)),
)
