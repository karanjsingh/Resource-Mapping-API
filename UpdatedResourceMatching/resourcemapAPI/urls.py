from django.urls import path
from . import views
# from .views import addTemClass
urlpatterns = [
    path('', views.getData),
    path('emp/', views.getEmpData),
    path('add/', views.addresource),
    path('map/', views.mapResource),
    path('clear/', views.clear),
    path('detail/<int:pk>/', views.detailItem),
    
    
]
