from django.shortcuts import render,redirect
import requests
from .models import Weather
from django.db import connection
import datetime as dt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def authication(city):
   api_key=get()
   weather_url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
   response=requests.get(weather_url)
   data=response.json()
   return data
def get():
   api_key="737f3b673bbbf96be7ba3490c827f249"
   return api_key

def get_weather(request):
  weather_data=Weather.objects.all().order_by("-date_time")
  if request.method=="POST":
    if "submit" in request.POST:
        city=request.POST["city"]
        if city:
          api_key=get()
          uv_url=f'http://api.openweathermap.org/data/2.5/uvi?lat={{lat}}&lon={{lon}}&appid={api_key}'
          air_quality_url=f'http://api.openweathermap.org/data/2.5/air_pollution?lat={{lat}}&lon={{lon}}&appid={api_key}'
          data=authication(city)
          if data["cod"] =="404":
              context={"error": "CITY NOT FOUND 404 ERROR"}
          else:
              Temperature=int(round(data["main"]["temp"]))
              Description=data["weather"][0]["description"]
              icon=data["weather"][0]["icon"]
              humidity=int(round(data["main"]["humidity"]))
              wind_speed=int(round(data["wind"]["speed"]))
              wind_direction=int(round(data["wind"]["deg"]))
              lat=data["coord"]["lat"]
              long=data["coord"]["lon"]
              Feeling_temp=int(round(data["main"]["feels_like"]))
              Min_temp=int(round(data["main"]["temp_min"]))
              Max_temp=int(round(data["main"]["temp_max"]))

              uv_response=requests.get(uv_url.format(lat=lat,lon=long))
              uv_data=uv_response.json()
              uv_index=uv_data["value"]
           
              air_response=requests.get(air_quality_url.format(lat=lat,lon=long))
              air_data=air_response.json()
              air_quality=air_data["list"][0]["main"]["aqi"]
           
            # to save them database
            
              storing=Weather(city=city,temperature=Temperature,Feeling_temp=Feeling_temp,Min_temp=Min_temp,Max_temp=Max_temp,description=Description,icon=icon,humidity=humidity,wind_speed=wind_speed,wind_direction=wind_direction,uv_index=uv_index,air_quality=air_quality,date_time=dt.datetime.now())
              storing.save()
            
              context=({"city":city,"temperature":Temperature,"Feeling":Feeling_temp,"Min_temp":Min_temp,"Max_temp":Max_temp,"description":Description,"icon":icon,"humidity":humidity,"wind_speed":wind_speed,"wind_direction":wind_direction,"uv_index":uv_index,"air_quality_index":air_quality,"latitude":lat,"longitude":long})

          return render(request,"weather/weather.html",context)
        else:
           return render(request,"weather/weather.html",{"error":"NO CITY MENTIONED PLEASE CHECK AGAIN"})
  
    elif "show" in request.POST:
       
      city=request.POST["city"]
      if city:
        query="SELECT * FROM weather_Weather WHERE city=%s ORDER BY date_time DESC;"
        weather_data=Weather.objects.raw(query,[city])
        return render(request,"weather/show_database.html",{"weather_data":weather_data}) 
      return render(request,"weather/weather.html",{"error":"NO CITY SPECIFIED IN FIELD CHECK AGAIN"})
       
  
    elif "search" in request.POST:

      temp=request.POST["temp"]
      if temp:
        query="SELECT id,city,temperature FROM weather_Weather where temperature=%s order by temperature desc;"
        weather_data=Weather.objects.raw(query,[temp])
        return render(request,"weather/search.html",{"weather_data":weather_data})
      else:
        return render(request,"weather/weather.html",{"error":"NO TEMPERATURE SPECIFIED IN FIELD CHECK AGAIN"})
    
    elif "Predict" in request.POST:
      city=request.POST["city"]
      if city:
          query="SELECT id,city,temperature FROM weather_Weather WHERE city=%s ORDER BY  date_time DESC;"
          history_data=Weather.objects.raw(query,[city])
          if history_data:
              date=np.array([i.date_time.timestamp() for i in history_data]).reshape(-1,1)
              temperature=np.array([i.temperature for i in history_data])
              model=LinearRegression().fit(date,temperature)
              next_day=dt.datetime.now()+dt.timedelta(days=1) #timedelta-->for duration of day
              predicted_temp=model.predict([[next_day.timestamp()]])[0]
              context={"city":city,"predicted_temp":int(round(predicted_temp))}
              return render(request,"weather/predict.html",context)
          else:
            df=pd.read_csv("F:\\Djangoprj\\project\\weather_prediction\\templates\\weather\\dataset.csv")
            data=pd.to_datetime(df["last_updated"])
            country_data=df[df["country"]==city]
            if not country_data.empty:
               
               date_update=np.array([(pd.to_datetime(d)).timestamp() for d in country_data["last_updated"]]).reshape(-1,1)
               temperature_update=np.array(country_data["temperature_celsius"])
               model=LinearRegression().fit(date_update,temperature_update)
               next_day=dt.datetime.now()+dt.timedelta(days=1) #timedelta-->for duration of day
               predicted_temp=model.predict([[next_day.timestamp()]])[0]
               context={"city":city,"predicted_temp":int(round(predicted_temp))}
               return render(request,"weather/predict.html",context)   
            else:
               data=authication(city)
               if data["cod"] =="404":
                context={"error": "CITY NOT FOUND 404 ERROR"}
               else:
                Temperature=int(round(data["main"]["temp"]))
                storing=Weather(city=city,temperature=Temperature,Feeling_temp=None,Min_temp=None,Max_temp=None,description=None,icon=None,humidity=None,wind_speed=None,wind_direction=None,uv_index=None,air_quality=None,date_time=dt.datetime.now())
                storing.save()
                query="SELECT id,city,temperature FROM weather_Weather WHERE city=%s ORDER BY  date_time DESC;"
                history_data=Weather.objects.raw(query,[city])
                if history_data:
                  date=np.array([i.date_time.timestamp() for i in history_data]).reshape(-1,1)
                  temperature=np.array([i.temperature for i in history_data])
                  model=LinearRegression().fit(date,temperature)
                  next_day=dt.datetime.now()+dt.timedelta(days=1) #timedelta-->for duration of day
                  predicted_temp=model.predict([[next_day.timestamp()]])[0]
                  context={"city":city,"predicted_temp":int(round(predicted_temp))}
               return render(request,"weather/predict.html",context)
          
               
      else: 
        return render(request,"weather/weather.html",{"error":"NO COUNTRY OR CITY IS MENTIONED"})
  return render(request,"weather/weather.html")
