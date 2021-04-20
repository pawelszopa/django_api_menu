from rest_framework import serializers

from menu.models import Menu, Dish


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        depth = 1


class DishSerializer(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), many=True)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'description', 'price', 'prep_time', 'is_vegetarian', 'image', 'menu')
