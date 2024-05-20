from django.db import models

# Create your models here.
class DailyWords(models.Model):
    day = models.IntegerField(unique=True)
    words = models.TextField()
    def __str__(self):
        return f"WordIndex {self.id}"