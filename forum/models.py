from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Rent(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own")
    title = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    price = models.BigIntegerField()
    quota = models.SmallIntegerField()
    occupant = models.ManyToManyField(User, related_name="rent")
    photo = models.ImageField(upload_to="images/")
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_closed = models.BooleanField(default="false")

    def __str__(self) -> str:
        return f"{self.owner}: ({self.title})"



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, related_name="comment")
    content = models.TextField()

    def __str__(self) -> str:
        return f"{self.rent.title} ({self.author})"

