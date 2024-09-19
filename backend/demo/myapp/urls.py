from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'SolarEnergyData', views.SolarEnergyDataViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('add_data/', views.excel_input_view, name='excel_view'),
    path('solar/', views.view_solar_data, name='view_solar_data'),
]
