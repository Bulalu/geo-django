from django.shortcuts import render,HttpResponse
from django.views.generic import View
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from django.views.generic import ListView, DetailView
import folium

from .utils import get_geo, get_center_coordinates, get_zoom
from .models import Measurement
from .forms import MeasurementForm
# Create your views here.


class MeasurementListView(ListView):
    model = Measurement
    

class MeasurementDetailView(DetailView):
    model = Measurement


class CalculateDistanceView(View):
    model = Measurement
    template = 'measurement/main.html'
    geolocator = Nominatim(user_agent='measurement')
  
    ip = '41.75.210.240' #my location dar
    country, city, lat, lon = get_geo(ip)

    #location coordinates and location(city)
    location_lat ,location_lon = lat,lon
    location_cord =(location_lat,location_lon)
    location = geolocator.geocode(city) #location and location are be used at post method
    
    
    def get(self,request):
        form = MeasurementForm()

        #initial folium
        m = folium.Map(width=800, height=500, location=get_center_coordinates(self.lat,self.lon), zoom_start=12)
        #location marker
        folium.Marker(location=self.location_cord, tooltip='click here', popup=self.city['city'],
                    icon=folium.Icon(color='purple')).add_to(m)
                        
        m = m._repr_html_()

        ctx = {'form':form, 'map':m}
        return render(request, self.template, ctx)

    def post(self,request):
       
        form = MeasurementForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            destination_ = form.cleaned_data.get('destination')
            destination = self.geolocator.geocode(destination_)
            #destination coordinates
            d_lat =  (destination.latitude)
            d_lon =  (destination.longitude)
            destination_cord = (d_lat,d_lon)

            #distance calculation in km with 2 dec places
            distance = round(geodesic(self.location_cord,destination_cord).km,2)

            #folium map modification
            m = folium.Map(width=800, height=500, location=get_center_coordinates(self.lat,self.lon,d_lat,d_lon), zoom_start=get_zoom(distance))
            #location marker
            folium.Marker(location=self.location_cord, tooltip='click here', popup=self.city['city'],
                    icon=folium.Icon(color='purple')).add_to(m)
            #destination marker
            folium.Marker(location=destination_cord, tooltip='click here', popup=destination,
                    icon=folium.Icon(color='red', icon='cloud')).add_to(m)

            #draw line between location and distance
            line = folium.PolyLine(
                    locations = [self.location_cord, destination_cord], 
                    weight = 2,
                    color = 'blue' 
                    )
            m.add_child(line)
            m = m._repr_html_()


            instance.location = self.location
            instance.distance = distance
            instance.save()

        form = MeasurementForm()
        
        
        ctx =  { 'form':form, 'map':m, 'distance':distance, 'destination':destination}
        return render(request, self.template, ctx)


