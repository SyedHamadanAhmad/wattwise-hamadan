from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('todos/', views.todos, name='todos'),  
    path('add/', views.add_todo, name='add_todo'), 
    path('cf/', views.cat_facts, name='cat facts'), 
    path('add_data/', views.excel_input_view, name='excel_view'), 
    path('solar/', views.view_solar_data, name='view_solar_data'),
]