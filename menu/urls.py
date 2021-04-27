from django.conf.urls import url
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from menu import views


app_name = 'menu'

urlpatterns = [
    path('private/menu/', views.MenuListView.as_view(), name='private_menu'),
    path('private/menu/<int:pk>', views.MenuDetailedView.as_view(), name='private_menu_detail'),
    path('private/dish/', views.DishListView.as_view(), name='private_dish'),
    path('private/dish/<int:pk>', views.DishDetailedView.as_view(), name='private_dish_detail'),
    path('public/menu/', views.PublicMenuListView.as_view(), name='public_menu'),
    path('public/menu/<int:pk>', views.PublicMenuView.as_view(), name='public_menu_detail'),

]
