from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.servers.basehttp import FileWrapper
from comicLibrary.models import ComicSeries, Comic
from comicLibrary.library_helpers import get_comic_page
import os
import mimetypes

# Create your views here.
def index(request):
    serieses = ComicSeries.objects.all()
    context = {"serieses" : serieses}
    return render(request, "comicLibrary/index.html", context)

def detail(request, series_id):
    s = get_object_or_404(ComicSeries, pk=series_id)
    comics = s.comic_set.all()
    return render(request, 'comicLibrary/detail.html', {'series': s, 'comics': comics})

#This will need to be modified to display mode
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

def comic_viewer(request, comic_id, page_num=1):
    comic = get_object_or_404(Comic, pk=comic_id)
    page_image = get_comic_page(comic, page_num)
    wrapper = FileWrapper(open(page_image,"rb"))
    response = HttpResponse(wrapper)
    response['Content-Type'] = 'application/force-download'
    response['Content-Disposition'] = 'attachment; filename="%s"' % page_image.split("/")[-1]
    response['Content-Length'] = os.path.getsize(comic.archive.path)
    return response

