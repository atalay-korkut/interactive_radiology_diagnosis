from django.db import models
from django.utils.timezone import now
# Create your models here.


class Query(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    clicks = models.IntegerField(default=0)
    outputText = models.CharField(max_length=200, default="")
    inputText = models.CharField(max_length=200, default="")
    createdAt = models.DateTimeField(default=now, editable=False)
