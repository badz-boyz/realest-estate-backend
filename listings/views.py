import requests
import os
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from dotenv import load_dotenv
from django.http import JsonResponse

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

@require_POST
@login_required
def save_listing(request, listing_id):
    saved_listing, created = SavedListing.objects.get_or_create(user=request.user, listing_id=listing_id)

    if created:
        return JsonResponse({'status': 'success', 'message': 'Listing saved successfully.'})
    else:
        return JsonResponse({'status': 'info', 'message': 'Listing was already saved.'})
    
@login_required
def get_saved_listings(request):
    saved_listings = SavedListing.objects.filter(user=request.user)
    # saved_ids = [listing.listing_id for listing in saved_listings]
    all_saved_listings = []
    for saved_listing in saved_listings:
        all_saved_listings.append(saved_listing)

    return JsonResponse(all_saved_listings)

class home_test(TemplateView):
    template_name = 'home.html'