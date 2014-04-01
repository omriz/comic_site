from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from comicLibrary.models import ComicSeries, Comic
from comicLibrary.library_helpers import get_comic_page
import os
import mimetypes

# Create your views here.
@login_required(login_url="/login")
def index(request):
    serieses = ComicSeries.objects.all()
    context = {"serieses" : serieses}
    return render(request, "comicLibrary/index.html", context)

@login_required(login_url="/login")
def detail(request, series_id):
    s = get_object_or_404(ComicSeries, pk=series_id)
    comics = s.comic_set.order_by('issue')
    return render(request, 'comicLibrary/detail.html', {'series': s, 'comics': comics})

#Deprecated view - we now use the comic_viewer
@login_required(login_url="/login")
def comic_download(request, comic_id):
    try:
        comic = Comic.objects.get(pk=comic_id)
    except Comic.DoesNotExist:
        raise Http404
    wrapper = FileWrapper(comic.archive)
    response = HttpResponse(wrapper)
    response['Content-Type'] = 'application/force-download'
    response['Content-Disposition'] = 'attachment; filename="%s"' % comic.archive.path.split("/")[-1]
    response['Content-Length'] = os.path.getsize(comic.archive.path)
    return response

@login_required(login_url="/login")
def comic_viewer(request, comic_id, page_num=1):
    page_num_int = int(page_num)
    comic = get_object_or_404(Comic, pk=comic_id)
    page_image = get_comic_page(comic, page_num_int)
    if page_image:
        return render(request, 'comicLibrary/comic_viewer.html', {'comic':comic, 'next_page':page_num_int+1, 'previous_page':page_num_int-1, 'page_image':page_image})
    else:
        return detail(request, comic.series.pk)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/login")

