from django.db import models

# Create your models here.

class Custom_user(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    number = models.IntegerField(unique=True)
    password = models.CharField(max_length=255)
    
    