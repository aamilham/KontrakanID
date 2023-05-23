from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('Laki-laki', 'Laki-laki'),
    ('Perempuan', 'Perempuan'),
)

class UserProfile(models.Model):
    photo = models.ImageField(upload_to="images", blank=False)
    status = models.TextField()
    gender = models.CharField(max_length=32, choices=GENDER_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", blank=True)
    link = models.TextField()

    

