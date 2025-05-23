from django.db import models
from django.contrib.auth.models import User

class WordPair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.CharField(max_length=255)
    output_text = models.TextField()

    def __str__(self):
        return f"{self.input_text} → {self.output_text}"
