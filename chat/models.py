from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

TASK_CHOICES = (("MESSAGE", "MESSAGE"), ("TASK","TASK"), ("CALENDER","CALENDER"),)


class Chat(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="chats")
    admin = models.ManyToManyField(User)
    picture = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_created", blank=True)
    datetime = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.ForeignKey("tasks.Task", on_delete=models.CASCADE ,blank=True, null=True)
    calender = models.ForeignKey("tasks.Calender", on_delete=models.CASCADE ,blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    
    datetime = models.DateTimeField(auto_now_add=True)

# class MessageTasks(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     tasks = models.ManyToManyField("tasks.Task", related_name="messagetasks")
#     datetime = models.DateField(auto_now=True)
