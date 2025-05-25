from django.db import models
from django.contrib.auth.models import User

class WordPair(models.Model):
    input_text = models.CharField(max_length=255)
    output_text = models.TextField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_posts', blank=True)
    is_public = models.BooleanField(default=True)


    def __str__(self):
        return self.title
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=100, default='UTC')  # Masalan: Asia/Tashkent
