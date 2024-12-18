
from django.db import models

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    description = models.TextField()

    def __str__(self):
        return self.file.name
    

# models.py



from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.email
