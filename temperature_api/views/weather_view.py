from datetime import datetime
from random import randrange
from django.views import View
from django.shortcuts import render, redirect
from temperature_api.models.weather_model import WeatherEntity
from temperature_api.repositories import WeatherRepository
from temperature_api.weatherSerializer import WeatherSerializer
from temperature_api.WeatherForm import WeatherForm


class WeatherView(View):
  def get(self, request):
    repository = WeatherRepository(collectionName='weathers')
    weathers = list(repository.getAll())
    serializer = WeatherSerializer(data=weathers, many=True)
    weathersData = []  # Defina um valor padrão para weathersData
    if serializer.is_valid():
        weathersData = serializer.data
        print(serializer.data)
    else:
        print(serializer.errors)
    return render(request, "home_data.html", {"weathers": weathersData})


class WeatherGenerate(View):
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weather = WeatherEntity(
            temperature=randrange(start=17, stop=40),
            date=datetime.now()
        )
        serializer = WeatherSerializer(data=weather.__dict__)
        if (serializer.is_valid()):
            repository.insert(serializer.data)
        else:
            print(serializer.errors)

        return redirect('Weather View')
    
class WeatherReset(View):
    def get(self, request): 
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteAll()

        return redirect('Weather View')
    
class WeatherInsert(View):
    def get(self, request):
        weatherForm = WeatherForm()

        return render(request, "create_previsao.html", {"form":weatherForm})
    
    def post(self, request):
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            serializer = WeatherSerializer(data=weatherForm.data)
            if (serializer.is_valid()):
                repository = WeatherRepository(collectionName='weathers')
                repository.insert(serializer.data)
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect('Weather View')