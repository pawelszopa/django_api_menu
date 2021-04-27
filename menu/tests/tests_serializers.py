from datetime import datetime

from django.test import TestCase

from menu.models import Menu, Dish
from menu.serializers import MenuSerializer, DishSerializer


class MenuSerializerTests(TestCase):

    def setUp(self):
        self.menu = Menu.objects.create(
            name='Test Menu 1',
            description='Test menu description 1',
        )
        self.dish_meat = Dish.objects.create(
            name='Test Meat Dish 1',
            description='Test meat description 1',
            price='10.50',
            prep_time=60,
            is_vegetarian=False,
        )
        self.menu.dish.add(self.dish_meat)

        self.serializer_input = Menu.objects.all()
        self.serializer = MenuSerializer(data=self.serializer_input, many=True)
        self.serializer.is_valid()

    def test_contain_expected_fields(self):
        data = self.serializer.data[0]
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'created_at', 'updated_at', 'dish'])

    def test_contain_expected_values(self):
        data = self.serializer.data[0]
        self.assertEqual(data['id'], self.menu.id)
        self.assertEqual(data['name'], self.menu.name)
        self.assertEqual(data['description'], self.menu.description)
        self.assertEqual(data['created_at'], datetime.strftime(self.menu.created_at, "%Y-%m-%d"))
        self.assertEqual(data['updated_at'], datetime.strftime(self.menu.updated_at, "%Y-%m-%d"))
        self.assertEqual(data['dish'][0]['id'], self.menu.dish.first().id)


class DishSerializerTests(TestCase):

    def setUp(self):
        self.menu = Menu.objects.create(
            name='Test Menu 1',
            description='Test menu description 1',
        )
        self.dish_meat = Dish.objects.create(
            name='Test Meat Dish 1',
            description='Test meat description 1',
            price='10.50',
            prep_time=60,
            is_vegetarian=False,
        )
        self.menu.dish.add(self.dish_meat)

        self.serializer_input = Dish.objects.all()
        self.serializer = DishSerializer(data=self.serializer_input, many=True)
        self.serializer.is_valid()

    def test_contain_expected_fields(self):
        data = self.serializer.data[0]
        self.assertCountEqual(data.keys(),
                              ['id', 'name', 'description', 'price', 'prep_time', 'is_vegetarian', 'image', 'menu'])

    def test_contain_expected_values(self):
        data = self.serializer.data[0]
        self.assertEqual(data['id'], self.dish_meat.id)
        self.assertEqual(data['name'], self.dish_meat.name)
        self.assertEqual(data['description'], self.dish_meat.description)
        self.assertEqual(data['price'], self.dish_meat.price)
        self.assertEqual(data['prep_time'], self.dish_meat.prep_time)
        self.assertEqual(data['is_vegetarian'], self.dish_meat.is_vegetarian)
        self.assertEqual(bool(data['image']), bool(self.dish_meat.image))
        self.assertEqual(data['menu'][0], self.dish_meat.menu.first().id)
