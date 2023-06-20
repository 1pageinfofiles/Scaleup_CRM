import requests
from django.shortcuts import render, HttpResponse
import dotenv
import os
from django.views.generic import TemplateView


dotenv.load_dotenv()
class GoogleMapDataExtractor(TemplateView):
    def get(self, request):
        return render(request, 'scaleupapp/gmapdataextractor.html')
    def post(self, request):
        api_key=os.getenv('GOOGLE_MAP_API_KEY')
        print("_______________________________________________")
        print(os.getenv('GOOGLE_MAP_API_KEY'))
        base_url='https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': request.POST.get('keyword_search'),
            'key': api_key,
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        print(data)
        return HttpResponse(data)