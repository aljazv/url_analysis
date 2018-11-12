from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import scraper.functions as fun
import requests

from scraper.serializers import UrlSerializer


# url = 'https://support.litmos.com/hc/en-us/articles/227739047-Sample-HTML-Header-Code'
# url = "https://pythonspot.com/wp-login.php?redirect_to=https%3A%2F%2Fpythonspot.com%2Fextract-links-from-webpage-beautifulsoup%2F"



@csrf_exempt
def url_info(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UrlSerializer(data=data)

        if serializer.is_valid():

            serializer.save()
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)
