import requests
from django.contrib.auth.models import User
import os
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.views.generic import TemplateView
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse
from .models import Listing
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
        'num_records': 10,
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
@require_http_methods(["POST"])
def user_login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        # Consider returning additional user info or a session token here
        return JsonResponse({'message': 'Login successful'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

@require_http_methods(["GET"])
def get_users(request):
    # Query the User model
    users = User.objects.all()
    # Serialize user data
    users_data = serializers.serialize('json', users, fields=('username',))
    # Return JSON response
    return JsonResponse(users_data, safe=False, status=200)



# def save_listing(request):
#     saved_listing = Listing.objects.create(user=request.body.user, address=request.body.address, description=request.body.description )
#     saved_listing.save()
#     return JsonResponse("Listing Saved")
@csrf_exempt
@require_POST
def save_listing(request):
    User = get_user_model()
    data = json.loads(request.body)
    print("request", data)
    try:
        data = json.loads(request.body)
        email = data.get('email')
        address = data.get('address')
        description = data.get('description')
        user = User.objects.get(email=email)
        listing, created = Listing.objects.get_or_create(user=user, address=address, defaults={'description': description})
        listing.save()
        
        return JsonResponse({'message': 'Listing saved successfully'}, status=201)
    # except CustomUser.DoesNotExist:
        # return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


     
class home_test(TemplateView):
    template_name = 'home.html'