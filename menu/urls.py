from django.urls import path

from menu import views


urlpatterns = [
    path('private/menu/', views.MenuListView.as_view(), name='private_menu'),
    path('private/menu/<int:pk>', views.MenuDetailedView.as_view(), name='private_menu_detail'),
    path('private/dish/', views.DishListView.as_view(), name='private_dish'),
    path('private/dish/<int:pk>', views.DishDetailedView.as_view(), name='private_dish_detail'),
    path('public/menu/', views.PublicMenuListView.as_view(), name='public_menu'),
    path('public/menu/<int:pk>', views.PublicMenuView.as_view(), name='public_menu_detail'),
    path('', views.EmailSender.as_view(), name='email'),
]