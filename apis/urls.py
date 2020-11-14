from django.urls import include, path, re_path
from rest_framework import routers

from apis.v1 import (
    WeatherSearchView,
)

urlpatterns = [
    path('v1/weather/search/', WeatherSearchView.as_view(), name='apis_v1_weather_search')
]