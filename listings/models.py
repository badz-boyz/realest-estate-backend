from django.db import models
from django.contrib.auth.models import User

class SavedListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.CharField(max_length=255)
    saved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.listing_id}"