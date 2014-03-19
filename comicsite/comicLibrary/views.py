from django.shortcuts import render
from django.http import HttpResponse, Http404
from comicLibrary.models import ComicSeries, Comic

# Create your views here.
def index(request):
    serieses = ComicSeries.objects.all()
    context = {"serieses" : serieses}
    return render(request, "comicLibrary/index.html", context)

def detail(request, series_id):
    try:
        s = ComicSeries.objects.get(pk=series_id)
    except ComicSeries.DoesNotExist:
        raise Http404
    return render(request, 'comicLibrary/detail.html', {'series': s})