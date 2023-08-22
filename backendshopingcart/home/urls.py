from django.urls import path
from . import views
urlpatterns = [
path('', views.home, name='home'),
path('cartitemadd',views.cartitemadd,name='home'),
path('cartview',views.cartview,name='cartview'),
path('cartcomplete',views.cartcomplete,name='cartcomplete'),
path('vieworderitem',views.vieworderitem,name='vieworderitem'),
]