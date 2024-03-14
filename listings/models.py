from django.db import models

class Listing(models.Model):
    user = models.TextField()
    address = models.TextField()
    description = models.TextField
    def __str__(self):
        return self.address