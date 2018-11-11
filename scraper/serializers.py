from rest_framework import serializers
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import scraper.functions as fun
import requests



class Url(object):
    def __init__(self, url, html_version, title, h1, h2, h3, h4, h5, h6, internal, external, inaccessible, has_loginform):
        self.url = url
        self.html_version = html_version
        self.title = title
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.h5 = h5
        self.h6 = h6
        self.internal = internal
        self.external = external
        self.inaccessible = inaccessible
        self.has_loginform = has_loginform


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    html_version = serializers.CharField(max_length=200, required=False)
    title = serializers.CharField(max_length=200, required=False)
    h1 = serializers.IntegerField(required=False)
    h2 = serializers.IntegerField(required=False)
    h3 = serializers.IntegerField(required=False)
    h4 = serializers.IntegerField(required=False)
    h5 = serializers.IntegerField(required=False)
    h6 = serializers.IntegerField(required=False)
    internal = serializers.IntegerField(required=False)
    external = serializers.IntegerField(required=False)
    inaccessible = serializers.IntegerField(required=False)
    has_loginform = serializers.BooleanField(required=False)

    def create(self, validated_data):

        url = validated_data["url"]

        r = requests.get(url)
        parsed_uri = urlparse(url)
        domain_name = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        soup = BeautifulSoup(r.text, "html.parser")
        # soup = BeautifulSoup(open("file2.html"), "html.parser")
        html_version = fun.html_version(soup)
        title = fun.page_title(soup)
        headings = fun.headings(soup)
        links = fun.number_of_links(soup, domain_name)
        has_loginform = fun.has_login(soup)

        return Url(**validated_data, html_version=html_version, title=title, **headings, **links, has_loginform = has_loginform)

    def update(self, instance, validated_data):
        return instance

