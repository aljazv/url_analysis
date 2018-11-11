from django.urls import path
from scraper import views

urlpatterns = [
    path('url/', views.url_info),
]