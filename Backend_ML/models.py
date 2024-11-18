from django.db import models

# Create your models here.


class Data(models.Model):
    post_id = models.CharField(max_length=50, primary_key=True, default="default")
    post_author = models.CharField(max_length=200, default="default")
    post_title = models.CharField(max_length=200, default="default")
    post_created = models.IntegerField(default=0)
    post_upvotes = models.IntegerField(default=0)
    comment_id = models.CharField(max_length=50, default="default")
    comment_author = models.CharField(max_length=200, default="default")
    comment_body = models.TextField(default="default")
    comment_created = models.IntegerField(default=0)
    comment_upvotes = models.IntegerField(default=0)
    subreddit = models.TextField(default="default")
    
    def __str__(self):
        return self.title