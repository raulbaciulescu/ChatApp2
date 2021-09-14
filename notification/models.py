from django.conf import settings
from django.db import models

# Create your models here.
class Notification(models.Model):
    fromm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fromm')
    to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to')
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
