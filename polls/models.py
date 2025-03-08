from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.title

class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.ManyToManyField(User, related_name='voted_options', blank=True)

    def __str__(self):
        return self.text
