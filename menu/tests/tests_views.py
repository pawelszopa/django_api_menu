import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from menu.models import Dish
from menu.serializers import DishSerializer

client = Client()


class DishViewSetTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(username="test", password="test")
        self.staff_user = get_user_model().objects.create_user(username="test1", password="test1", is_staff=True)
        self.dish_meat = Dish.objects.create(
            name="Test Meat Dish 1",
            description="Test meat description 1",
            price="10.50",
            prep_time=60,
            is_vegetarian=False,
            author=self.user,
        )
        self.dish_vege = Dish.objects.create(
            name="Test Vege Dish 1",
            description="Test vege description 1",
            price="10.50",
            prep_time=60,
            is_vegetarian=True,
            author=self.staff_user,
        )
        self.valid_dish = {
            "name": "123",
            "description": "123",
            "price": "123",
            "prep_time": 123,
            "is_vegetarian": False
        }

        self.invalid_dish = {
            "name": "123",
            "description": "123",
            "price": "123",
            "prep_time": 123
        }

    def test_get_all_dishes_not_logged_user(self):
        response = client.get(reverse('menu:dishes-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_dishes_logged_user(self):
        client.login(username='test', password='test')
        response = client.get(reverse('menu:dishes-list'))
        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_valid_dish_not_logged_user(self):
        response = client.post(
            reverse('menu:dishes-list'),
            data=json.dumps(self.valid_dish),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_valid_dish_logged_user(self):
        client.login(username='test', password='test')
        response = client.post(
            reverse('menu:dishes-list'),
            data=json.dumps(self.valid_dish),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_dish_logged_user(self):
        client.login(username='test', password='test')
        response = client.post(
            reverse('menu:dishes-list'),
            data=json.dumps(self.invalid_dish),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid_dish_not_logged_user(self):
        response = client.put(
            reverse('menu:dishes-detail', kwargs={'pk': self.dish_meat.pk}),
            data=json.dumps(self.valid_dish),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_valid_dish_logged_user(self):
        client.login(username='test', password='test')
        response = client.put(
            reverse('menu:dishes-detail', kwargs={'pk': self.dish_meat.pk}),
            data=json.dumps(self.valid_dish),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_valid_dish_logged_user_not_owner(self):
        client.login(username='test', password='test')
        response = client.put(
            reverse('menu:dishes-detail', kwargs={'pk': self.dish_vege.pk}),
            data=json.dumps(self.valid_dish),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_invalid_dish_logged_user(self):
        client.login(username='test', password='test')
        response = client.put(
            reverse('menu:dishes-detail', kwargs={'pk': self.dish_vege.pk}),
            data=json.dumps(self.invalid_dish),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_dish_not_logged_user(self):
        response = client.delete(
            reverse('menu:dishes-detail', kwargs={'pk': self.dish_meat.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_dish_logged_user(self):
        client.login(username='test', password='test')
        response = client.delete(
            reverse('menu:dishes-detail', kwargs={'pk': self.dish_meat.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_dish_logged_user_not_owner(self):
        client.login(username='test', password='test')
        response = client.delete(
            reverse('menu:dishes-detail', kwargs={'pk': self.dish_vege.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

