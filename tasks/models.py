from django.db import models
from django.contrib.auth import get_user_model

User =get_user_model()

# Create your models here.

TASK_CHOICES = (("Assignment", "Assignment"), ("Others","Others"),)

class Calender(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    datetime = models.DateTimeField(auto_now_add=True)
    


class Task(models.Model):
    calender = models.ForeignKey("tasks.Calender", on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateTimeField()
    datetime = models.DateTimeField(auto_now_add=True)
    additional_notes = models.TextField()
    type_type = models.CharField(choices=TASK_CHOICES, max_length=100)


