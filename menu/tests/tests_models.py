from django.db import DataError, IntegrityError
from django.test import TestCase

from menu.models import *


class MenuTests(TestCase):

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
        self.dish_vege = Dish.objects.create(
            name='Test vegetarian Dish 1',
            description='Test vegetarian description 1',
            price='12.50',
            prep_time=25,
            is_vegetarian=True,
        )
        self.menu.dish.add(self.dish_meat)
        self.menu.dish.add(self.dish_vege)

    def test_menu_creation(self):
        self.assertTrue(isinstance(self.menu, Menu))
        self.assertEqual(self.menu.name, 'Test Menu 1')
        self.assertEqual(self.menu.description, 'Test menu description 1')

    def test_menu_fields(self):
        self.assertEqual(
            [*self.menu.__dict__],
            ['_state', 'id', 'name', 'description', 'created_at', 'updated_at']
        )

    def test_menu_str(self):
        self.assertEqual(str(self.menu), 'Test Menu 1')

    def test_relationship(self):
        self.assertTrue(self.dish_meat in self.menu.dish.all())
        self.assertTrue(self.dish_vege in self.menu.dish.all())

    def test_create_menu_with_to_long_name(self):
        with self.assertRaises(DataError):
            test_menu = Menu.objects.create(
                name='x' * 257,
                description='Test menu description 1',
            )

    def test_create_menu_with_already_existing_name(self):
        with self.assertRaises(IntegrityError):
            test_menu = Menu.objects.create(
                name='Test Menu 1',
                description='Test menu description 1',
            )


class DishTests(TestCase):

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
        self.dish_vege = Dish.objects.create(
            name='Test vegetarian Dish 1',
            description='Test vegetarian description 1',
            price='12.50',
            prep_time=25,
            is_vegetarian=True,
        )
        self.menu.dish.add(self.dish_meat)
        self.menu.dish.add(self.dish_vege)

    def test_dish_creation(self):
        self.assertTrue(isinstance(self.dish_vege, Dish))
        self.assertTrue(isinstance(self.dish_vege, Dish))