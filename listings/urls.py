from django.urls import path
from .views import get_listings, home_test, create_user

urlpatterns = [
    path('', home_test.as_view(), name='home_test'),
    path('listings/<str:city>/', get_listings, name='listings'),
    path('signup/<str:email>/', create_user, name='create_user'),
    # path('save_listing/<str:listing_id>/', save_listing, name='save_listing'),
    # path('saved/', get_saved_listings, name='get_saved_listings')
]