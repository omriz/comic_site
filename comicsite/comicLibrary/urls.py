from django.conf.urls import patterns, url

from comicLibrary import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<series_id>\d+)/$', views.detail, name='detail'),
)