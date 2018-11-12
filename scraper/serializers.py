from rest_framework import serializers
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import scraper.functions as fun
import requests
from scraper.models import UrlModel
from datetime import timedelta
from django.utils import timezone


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    html_version = serializers.CharField(max_length=200, required=False, read_only=True)
    title = serializers.CharField(max_length=200, required=False, read_only=True)
    h1 = serializers.IntegerField(required=False, read_only=True)
    h2 = serializers.IntegerField(required=False, read_only=True)
    h3 = serializers.IntegerField(required=False, read_only=True)
    h4 = serializers.IntegerField(required=False, read_only=True)
    h5 = serializers.IntegerField(required=False, read_only=True)
    h6 = serializers.IntegerField(required=False, read_only=True)
    internal = serializers.IntegerField(required=False, read_only=True)
    external = serializers.IntegerField(required=False, read_only=True)
    inaccessible = serializers.IntegerField(required=False, read_only=True)
    has_login_form = serializers.BooleanField(required=False, read_only=True)

    def create(self, validated_data):

        url = validated_data["url"]

        # if we have cached web page
        if UrlModel.objects.filter(url=url).exists():

            existing_object = UrlModel.objects.get(url=url)

            # if cached web page is older than 1 day, recache

            if existing_object.created < (timezone.now()-timedelta(days=1)):
                r = requests.get(url)
                parsed_uri = urlparse(url)
                domain_name = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                soup = BeautifulSoup(r.text, "html.parser")
                html_version = fun.html_version(soup)
                title = fun.page_title(soup)
                headings = fun.headings(soup)
                links = fun.number_of_links(soup, domain_name, url)
                has_login_form = fun.has_login(soup)

                UrlModel.objects.filter(pk= existing_object.pk).update(**validated_data, html_version=html_version, title=title, **headings,
                                               **links, has_login_form=has_login_form, created=timezone.now())

            return existing_object

        # request webpage and go through all tasks
        try:
            r = requests.get(url)
            parsed_uri = urlparse(url)
            domain_name = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            soup = BeautifulSoup(r.text, "html.parser")
            html_version = fun.html_version(soup)
            title = fun.page_title(soup)
            headings = fun.headings(soup)
            links = fun.number_of_links(soup, domain_name, url)
            has_login_form = fun.has_login(soup)

            return UrlModel.objects.create(**validated_data, html_version=html_version, title=title, **headings,
                                           **links, has_login_form=has_login_form)

        except requests.ConnectionError as err:
            print("somethin:", err)
            raise Exception("THis should not happen")


    def update(self, instance, validated_data):
        return instance

    # error handling for is_valid() method. return false if connection can not be established
    def validate_url(self, value):
        try:
            r = requests.get(value)

            return value
        except requests.exceptions.Timeout as e:
            raise serializers.ValidationError("Network problem:  "+ str(e))
        except requests.exceptions.TooManyRedirects as e:
            raise serializers.ValidationError("Url was bad, try again: "+ str(e))
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError("Something went wrong: " + str(e))