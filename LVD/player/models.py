from django.db import models

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=6)
    birth = models.DateField()
    country = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class VideoIntroduction(models.Model):
    director = models.CharField(max_length=30)
    actors = models.ManyToManyField(Actor)
    content = models.CharField(max_length=500)

class Classification(models.Model):
    name = models.CharField(max_length=20)


class VideoInfo(models.Model):
    name = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    score = models.CharField(max_length=3) # range 0 to 100
    releaseDate = models.DateField()
    thumbnailsLoc = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    classification = models.ManyToManyField(Classification)
    introduction = models.ForeignKey(VideoIntroduction)


