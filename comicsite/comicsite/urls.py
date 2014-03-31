from django.conf.urls import patterns, include, url
from django.contrib import admin
from comicLibrary import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comicsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^comicLibrary/', include('comicLibrary.urls')),
    url(r'^comicLibrary/\d+/media/(?P<comic_id>\d+)/(?P<page_num>\d+)/$',views.comic_viewer, name='comic_viewer'),
    url(r'^login/','django.contrib.auth.views.login'),
    url(r'logout/',views.logout_page, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
