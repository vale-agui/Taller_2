from django.db import models

# create your models here

class Movie(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='movies/')
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Untitled Movie"