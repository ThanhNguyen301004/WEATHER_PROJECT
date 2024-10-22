from django.db import models

from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='img/')
    description = models.TextField()
    pdf = models.FileField(upload_to='pdf/')
    
    def __str__(self):
        return self.title
