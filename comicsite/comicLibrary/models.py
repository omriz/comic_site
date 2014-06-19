from django.db import models
from django.contrib import admin

# Create your models here.
class ComicSeries(models.Model):
    series = models.CharField(max_length=200)
    def __str__(self):
        return self.series

class Comic(models.Model):
    series = models.ForeignKey(ComicSeries)
    issue = models.IntegerField()
    archive = models.FileField(upload_to = "comics/")
    annual = models.BooleanField()
    def __str__(self):
        if self.annual:
            return u"Annual {0} #{1}".format(self.series, self.issue)
        else:
            return u"{0} #{1}".format(self.series, self.issue)
    
admin.site.register(ComicSeries)
admin.site.register(Comic)
