from django.db import models

# Create your models here.

class NationalId(models.Model):
    number = models.CharField(max_length=100)
   
    def __str__(self):
        return self.number
    
class Visit(models.Model):
    username = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return self.username
    

    
