from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from menu.models import Menu, Dish
from menu.serializers import MenuSerializer, DishSerializer


class MenuListView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = MenuSerializer
    model = Menu
    queryset = Menu.objects.all().prefetch_related('dish')


class MenuDetailedView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer
    model = Menu

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Menu.objects.filter(pk=pk).prefetch_related('dish')


class DishListView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = DishSerializer
    model = Dish
    queryset = Dish.objects.all()


class DishDetailedView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DishSerializer
    model = Dish

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Dish.objects.filter(pk=pk)


class PublicMenuListView(ListAPIView):
    serializer_class = MenuSerializer
    model = Menu

    def get_queryset(self):
        filter_name = self.request.GET.get('fn')
        filter_menu_creation_gte = self.request.GET.get('cgte')
        filter_menu_creation_lte = self.request.GET.get('clte')
        filter_menu_updated_gte = self.request.GET.get('ugte')
        filter_menu_updated_lte = self.request.GET.get('ulte')

        sort_name = self.request.GET.get('sn')
        sort_dish = self.request.GET.get('sd')

        queryset = self.model.objects.annotate(dish_number=Count('dish')).filter(dish_number__gt=0)

        if filter_name:
            queryset = queryset.filter(name__icontains=filter_name)

        if filter_menu_creation_gte:
            queryset = queryset.filter(created_at__gte=filter_menu_creation_gte)

        if filter_menu_creation_lte:
            queryset = queryset.filter(created_at__lte=filter_menu_creation_lte)

        if filter_menu_updated_gte:
            queryset = queryset.filter(updated_at__gte=filter_menu_updated_gte)

        if filter_menu_updated_lte:
            queryset = queryset.filter(updated_at__lte=filter_menu_updated_lte)

        if sort_name == 'DESC':
            queryset = queryset.order_by('-name')

        if sort_name == "ASC":
            queryset = queryset.order_by('name')

        if sort_dish == 'DESC':
            queryset = queryset.order_by('-dish_number')

        if sort_dish == 'ASC':
            queryset = queryset.order_by('dish_number')

        return queryset


class PublicMenuView(RetrieveAPIView):
    serializer_class = MenuSerializer
    model = Menu

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Menu.objects.filter(pk=pk).prefetch_related('dish')
