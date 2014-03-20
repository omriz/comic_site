from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.servers.basehttp import FileWrapper
from comicLibrary.models import ComicSeries, Comic
import os
import mimetypes

# Create your views here.
def index(request):
    serieses = ComicSeries.objects.all()
    context = {"serieses" : serieses}
    return render(request, "comicLibrary/index.html", context)

def detail(request, series_id):
    try:
        s = ComicSeries.objects.get(pk=series_id)
        comics = s.comic_set.all()
    except ComicSeries.DoesNotExist:
        raise Http404
    return render(request, 'comicLibrary/detail.html', {'series': s, 'comics': comics})

def comic_download(request, comic_id):
    try:
        comic = Comic.objects.get(pk=comic_id)
    except Comic.DoesNotExist:
        raise Http404
    wrapper = FileWrapper(comic.archive)
    #fp = open(comic.archive.path, 'rb')
    #response = HttpResponse(fp)
    response = HttpResponse(wrapper)
    response['Content-Type'] = 'application/force-download'
    #response['X-Sendfile'] = comic.archive.path
    response['Content-Disposition'] = 'attachment; filename="%s"' % comic.archive.path.split("/")[-1]
    response['Content-Length'] = os.path.getsize(comic.archive.path)
    return response