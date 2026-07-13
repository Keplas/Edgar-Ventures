from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sectors/', views.sectors, name='sectors'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news, name='news'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('careers/', views.careers, name='careers'),
    path('privacy/', views.privacy, name='privacy'),
    # Products hub + sectors
    path('products/', views.products_hub, name='products_hub'),
    path('products/technology/', views.products_technology, name='products_technology'),
    path('products/agriculture/', views.products_agriculture, name='products_agriculture'),
    path('products/trade/', views.products_trade, name='products_trade'),
    path('products/infrastructure/', views.products_infrastructure, name='products_infrastructure'),
    # Agriculture shop
    path('agriculture/shop/', views.agri_shop, name='agri_shop'),
    path('agriculture/shop/<slug:slug>/', views.agri_product, name='agri_product'),
    path('agriculture/cart/', views.agri_cart, name='agri_cart'),
    path('agriculture/cart/add/<int:pk>/', views.agri_cart_add, name='agri_cart_add'),
    path('agriculture/cart/remove/<int:pk>/', views.agri_cart_remove, name='agri_cart_remove'),
    path('agriculture/cart/update/', views.agri_cart_update, name='agri_cart_update'),
    path('agriculture/checkout/', views.agri_checkout, name='agri_checkout'),
    path('agriculture/order/success/<str:order_number>/', views.agri_order_success, name='agri_order_success'),
    path('agriculture/order/track/', views.agri_order_track, name='agri_order_track'),
    # SEO
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
