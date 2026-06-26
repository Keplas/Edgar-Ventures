from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('sectors/', views.sectors, name='sectors'),
    path('news/', views.news, name='news'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('careers/', views.careers, name='careers'),
    path('privacy/', views.privacy, name='privacy'),
]
