from django.urls import path

from menu import views

urlpatterns = [
    path('private/menu/', views.MenuListView.as_view()),
    path('private/menu/<int:pk>', views.MenuDetailedView.as_view()),
    path('private/dish/', views.DishListView.as_view()),
    path('private/dish/<int:pk>', views.DishDetailedView.as_view()),
    path('public/menu/', views.PublicMenuListView.as_view()),
    path('public/menu/<int:pk>', views.PublicMenuView.as_view()),
]