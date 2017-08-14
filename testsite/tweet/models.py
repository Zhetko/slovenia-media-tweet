from django.db import models

class Tweet(models.Model):
    tweet_text_orig = models.CharField(max_length=500)
    tweet_text_lem = models.CharField(max_length=500)
    tweet_text_stop = models.CharField(max_length=500)
    tweet_date = models.DateField('date tweet published')
    tweet_user = models.CharField(max_length=100)
