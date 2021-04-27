from django.conf.urls import url
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from menu import views

schema_view = get_schema_view(
    openapi.Info(
        title="Menu API",
        default_version='v1',
        description="Endpoints of Car API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

app_name = 'menu'

urlpatterns = [
    path('private/menu/', views.MenuListView.as_view(), name='private_menu'),
    path('private/menu/<int:pk>', views.MenuDetailedView.as_view(), name='private_menu_detail'),
    path('private/dish/', views.DishListView.as_view(), name='private_dish'),
    path('private/dish/<int:pk>', views.DishDetailedView.as_view(), name='private_dish_detail'),
    path('public/menu/', views.PublicMenuListView.as_view(), name='public_menu'),
    path('public/menu/<int:pk>', views.PublicMenuView.as_view(), name='public_menu_detail'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
