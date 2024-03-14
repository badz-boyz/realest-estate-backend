import requests
import os
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import CustomUser, Listing
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse


def parse_listings(listings):
    parsed_listings = {}
    for record in listings:
        parsed_listings[record["address"]] = {
            "city": record["city"],
            "description": record["descriptions"][0]["value"]
        }
    return parsed_listings

def get_listings(request, city=None):  
    load_dotenv()
    api_key = os.environ.get('API_KEY')  
    url = 'https://api.datafiniti.co/v4/properties/search'
    query = f'country:US AND propertyType:"Single Family Dwelling" AND city:"{city}"'
    request_headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json',
    }
    request_data = {
        'query': query,
        'format': 'JSON',
        'num_records': 3,
        'download': False
    }
    response = requests.post(url, json=request_data, headers=request_headers)
    data = response.json()
    listings = parse_listings(data["records"])
    return JsonResponse(listings) 

def create_user(request, email):
        # new_user = CustomUser(email=email)
        # new_user.save()
        return HttpResponse(f'User {email} created')

def save_listing(request, email, address, description):
     new_listing = Listing(address=address, description=description)
     user = CustomUser.objects.get(email=email)
     user.saved_listings.add(new_listing)
     
class home_test(TemplateView):
    template_name = 'home.html'