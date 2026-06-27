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
    # Products & Services
    path('products/', views.products_hub, name='products_hub'),
    path('products/technology/', views.products_technology, name='products_technology'),
    path('products/agriculture/', views.products_agriculture, name='products_agriculture'),
    path('products/trade/', views.products_trade, name='products_trade'),
    path('products/infrastructure/', views.products_infrastructure, name='products_infrastructure'),
]
