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
        sort_name = self.request.GET.get('sn')
        sort_dish_gte = self.request.GET.get('gte') if self.request.GET.get('gte') else 0
        sort_dish_lte = self.request.GET.get('lte') if self.request.GET.get('lte') else 99999

        filter_name = self.request.GET.get('fn')
        filter_created = self.request.GET.get('fcr')
        filter_update = self.request.GET.get('upd')

        if sort_name:
            queryset = self.model.objects.filter(name__icontains=sort_name)

        else:
            queryset = Menu.objects.filter(dish__isnull=False)

        queryset = queryset.annotate(dish_number=Count('dish')).filter(dish_number__gte=sort_dish_gte,
                                                                       dish_number__lte=sort_dish_lte)
        if filter_name == 'DESC':
            queryset = queryset.order_by('-name')
        if filter_name == "ASC":
            queryset = queryset.order_by('name')

        if filter_created == 'DESC':
            queryset = queryset.order_by('-created_at')
        if filter_created == "ASC":
            queryset = queryset.order_by('created_at')

        if filter_update == 'DESC':
            queryset = queryset.order_by('-updated_at')
        if filter_update == "ASC":
            queryset = queryset.order_by('updated_at')

        return queryset


class PublicMenuView(RetrieveAPIView):
    serializer_class = MenuSerializer
    model = Menu

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Menu.objects.filter(pk=pk).prefetch_related('dish')
