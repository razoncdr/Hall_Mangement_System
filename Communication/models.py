from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)  # Automatically set the date when the notice is created
    
    def __str__(self):
        return self.title
