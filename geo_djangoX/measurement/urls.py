
from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'measurement'

urlpatterns = [
    path('',views.CalculateDistanceView.as_view(), name='all'),
    path('lookup/',views.MeasurementListView.as_view(), name ='measurement_list'),
    path('lookup/<int:pk>/detail',views.MeasurementDetailView.as_view(), name ='measurement_detail'),
    path('thanks/',TemplateView.as_view(template_name='measurement/thanks.html'), name='thanks')
]