from rest_framework import serializers

from menu.models import Menu, Dish


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ("author", )
        read_only_fields = ('created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super(MenuSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'GET':
            self.Meta.depth = 1
        else:
            self.Meta.depth = 0

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = ('id', 'name', 'description', 'price', 'prep_time', 'is_vegetarian', 'image')

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)