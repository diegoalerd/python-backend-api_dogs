from django.db import models
 
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)