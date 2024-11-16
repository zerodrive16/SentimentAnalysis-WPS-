from django.db import models

# Create your models here.


class Data(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    link_author = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=1000)
    time_posted = models.IntegerField()
    body_information = models.TextField()

    def __str__(self):
        return self.title