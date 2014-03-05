from django.db import models

# Create your models here.
class Comic(models.Model):
    series = models.CharField(max_length=200)
    issue_number = models.IntegerField()
    archive_location = models.FilePathField(path=None)
    # If the path for the cached location is not None it means we have it in the cache
    cached_location = models.FilePathField(path=None)