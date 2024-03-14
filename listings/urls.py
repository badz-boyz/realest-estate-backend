from django.urls import path
from .views import get_listings, home_test, create_user, get_users
from . import views

urlpatterns = [
    path('', home_test.as_view(), name='home_test'),
    path('listings/<str:city>/', get_listings, name='listings'),
    path('signup/', create_user, name='create_user'),
    path('signup/<str:city>/', create_user, name='create_user'),
    path('users/', get_users, name='get_users'),
    path('login/', views.user_login, name='user_login'),
    # path('save_listing/<str:listing_id>/', save_listing, name='save_listing'),
    # path('saved/', get_saved_listings, name='get_saved_listings')
]