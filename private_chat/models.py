from django.conf import settings
from django.db import models

# Create your models here.

class PrivateChat(models.Model):
    first = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='first')
    second = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='second')

class PrivateMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)