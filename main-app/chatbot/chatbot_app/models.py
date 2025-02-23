from django.db import models

# Create your models here.
class Chatbot(models.Model):
    query=models.CharField(max_length=500)
    response=models.CharField(max_length=500)
    #image=models.ImageField(upload_to='images/')
    def __str__(self):
        return self.query