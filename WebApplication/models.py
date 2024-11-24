from django.db import models

# Create your models here.


class Data(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=0)
    post_id = models.CharField(max_length=50)
    post_author = models.CharField(max_length=200)
    post_title = models.CharField(max_length=200)
    post_created = models.IntegerField()
    post_upvotes = models.IntegerField()
    comment_id = models.CharField(max_length=50)
    comment_author = models.CharField(max_length=200)
    comment_body = models.TextField()
    comment_created = models.IntegerField()
    comment_upvotes = models.IntegerField()
    subreddit = models.TextField()
    
    def __str__(self):
        return self.post_title