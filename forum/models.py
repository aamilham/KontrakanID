from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class Rent(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own")
    title = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    price = models.BigIntegerField(validators=[MinValueValidator(0)])
    quota = models.SmallIntegerField(validators=[MinValueValidator(1)])
    occupant = models.ManyToManyField(User, related_name="waiting_list", blank=True)
    photo = models.ImageField(upload_to="images/")
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner}: ({self.title})" 

    def get_remainder_quota(self):
        return self.quota - len(self.occupant.all())
    
    def is_already_in(self, new_occupant):
        for user in self.occupant.all():
            if user.id == new_occupant.id:
                return True
        return False
    
    def close_if_full(self):
        if self.get_remainder_quota() <= 0:
            self.is_closed = True
            self.save()
    
    def open_if_not_full(self):
        if self.get_remainder_quota() > 0:
            self.is_closed = False
            self.save()

    def add_occupant(self, new_occupant):
        if self.get_remainder_quota() > 0 and not self.is_already_in(new_occupant):
            self.occupant.add(new_occupant)
            self.save()
            self.close_if_full()
            return True
        return False
    
    def delete_occupant(self, ocp):
        self.occupant.remove(ocp)
        self.save()
        self.open_if_not_full()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, related_name="comment")
    content = models.TextField()

    def __str__(self) -> str:
        return f"{self.rent.title} ({self.author})"

