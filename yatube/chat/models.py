from django.db import models


class Message(models.Model):
    message = models.TextField()
    username = models.CharField(max_length=10)
    pub_date = models.DateTimeField(auto_now_add=True)
