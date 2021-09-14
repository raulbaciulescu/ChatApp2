from django.db import models
from django.conf import settings


class PublicChatRoom(models.Model):
    title = models.CharField(max_length=120, unique=True, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, help_text="users who are connected to the chat")

    def __str__(self):
        return self.title

    def connect_user(self, user):
        """
        add an user in room
        """
        if not user in self.users.all():
            self.users.add(user)
            self.save()


    def disconnect_user(self, user):
        """
        remove an user
        """
        if user in self.users.all():
            self.users.remove(user)
            self.save()



class PublicChatMessageManager(models.Manager):
    def by_room(self, room):
        query_set = PublicChatMessage.objects.filter(room=room).order_by('-timestamp')
        return query_set

class PublicChatMessage(models.Model):
    '''
    Chat message created by a user inside a PublicChat room (foreign key)
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)
    objects = PublicChatMessageManager()

    def __str__(self):
        return self.content