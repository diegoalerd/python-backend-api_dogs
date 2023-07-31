from django.db import models
 
class Breeds(models.Model):
    breedsId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)