from django.contrib import admin
from .models import Listing, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Listing)