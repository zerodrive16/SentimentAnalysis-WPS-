from django.db import models


# Create your models here.


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.CharField(max_length=50)
    post_author = models.CharField(max_length=200)
    post_title = models.CharField(max_length=200)
    post_created = models.IntegerField()
    post_up_votes = models.IntegerField()
    c_id = models.IntegerField()
    comment_id = models.CharField(max_length=50)
    comment_author = models.CharField(max_length=100)
    comment_body = models.TextField()
    comment_body_adjusted = models.TextField()
    comment_created = models.IntegerField()
    comment_up_votes = models.IntegerField(default=1)
    subreddit = models.CharField(max_length=15)
    comment_personal_labels = models.IntegerField(null=False, default=1)
    comment_bert_labels = models.IntegerField()

    def __str__(self):
        return self.post_title