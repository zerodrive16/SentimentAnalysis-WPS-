from django.db import models

# Create your models here.


class Data(models.Model):
    feature_1 = models.FloatField()
    feature_2 = models.FloatField()
    target = models.FloatField()

    def __str__(self):
        return f'{self.feature_1}, {self.feature_2}, {self.target}'