from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets

from menu.models import Menu, Dish
from menu.serializers import MenuSerializer, DishSerializer
from menu.permissions import IsOwnerOrStaffOrAdmin, IsOwnerOrStaffOrAdminOrReadOnly


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all().prefetch_related('author')
    permission_classes = [IsOwnerOrStaffOrAdmin]


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all().annotate(dishes_count=Count('dish')).prefetch_related('dish')
    permission_classes = [IsOwnerOrStaffOrAdminOrReadOnly]

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = {
        'name': ["exact"],
        'updated_at': ["exact"],
        'created_at': ['lte', 'gte'],
    }
    ordering_fields = ['name', 'dishes_count']
    ordering = ['pk']

    def get_queryset(self):
        print(self.request.user.get_user_permissions())
        if self.request.user.get_user_permissions():
            queryset = Menu.objects.all().annotate(dishes_count=Count('dish')).prefetch_related('dish')
        else:
            queryset = Menu.objects.all().annotate(dishes_count=Count('dish')).filter(
                dishes_count__gt=0).prefetch_related('dish')
        return queryset
