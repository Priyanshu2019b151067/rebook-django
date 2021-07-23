from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
