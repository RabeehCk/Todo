from django.db import models
from django.contrib.auth.models import User


class taskmodel(models.Model):

    task_name = models.CharField(max_length=50)
    task_description = models.TextField(null=False)
    created_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name