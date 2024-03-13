from django.db import models
from django.utils.translation import gettext_lazy as _

class Listing(models.Model):
    address = models.TextField()
    description = models.TextField

    def __str__(self):
        return self.address

class CustomUser(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    saved_listings = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return self.email