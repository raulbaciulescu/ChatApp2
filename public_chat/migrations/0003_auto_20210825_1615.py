# Generated by Django 3.2 on 2021-08-25 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_chat', '0002_privatechat_privatemessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatemessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='user',
        ),
        migrations.DeleteModel(
            name='PrivateChat',
        ),
        migrations.DeleteModel(
            name='PrivateMessage',
        ),
    ]
