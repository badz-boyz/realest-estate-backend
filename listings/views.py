import requests
from django.contrib.auth.models import User
import os
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse
import json

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

@csrf_exempt
@require_POST
def create_user(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        # Optionally add email validation here
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        return JsonResponse({'message': 'User created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_POST
def save_listing(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        address = data.get('address')
        description = data.get('description')

        user = CustomUser.objects.get(email=email)
        listing, created = Listing.objects.get_or_create(address=address, defaults={'description': description})
        user.saved_listings.add(listing)
        
        return JsonResponse({'message': 'Listing saved successfully'}, status=201)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

     
class home_test(TemplateView):
    template_name = 'home.html'