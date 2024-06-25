from django.urls import path
from . import views

urlpatterns=[
    path("",views.get_weather,name="get_weather"),
    path("show_database/",views.get_weather,name="show_database"),
    path("search/",views.get_weather,name="search"),
    path("predict/",views.get_weather,name="predict"),
]