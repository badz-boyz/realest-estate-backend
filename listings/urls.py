from django.urls import path
from .views import get_listings, save_listing,get_saved_listings, home_test

urlpatterns = [
    path('', home_test.as_view(), name='home_test'),
    path('listings/<str:city>/', get_listings, name='listings'),
    path('save_listing/<str:listing_id>/', save_listing, name='save_listing'),
    path('saved/', get_saved_listings, name='get_saved_listings')
]