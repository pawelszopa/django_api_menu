import json
from datetime import timedelta, date, datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from menu.models import Dish, Menu
from menu.serializers import DishSerializer

client = Client()


class DishViewSetTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="test"
        )
        self.staff_user = get_user_model().objects.create_user(
            username="test1", password="test1", is_staff=True
        )
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
            "is_vegetarian": False,
        }

        self.invalid_dish = {
            "name": "123",
            "description": "123",
            "price": "123",
            "prep_time": 123,
        }

    def test_get_all_dishes_not_logged_user(self):
        response = client.get(reverse("menu:dishes-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_dishes_logged_user(self):
        client.login(username="test", password="test")
        response = client.get(reverse("menu:dishes-list"))
        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_valid_dish_not_logged_user(self):
        response = client.post(
            reverse("menu:dishes-list"),
            data=json.dumps(self.valid_dish),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_valid_dish_logged_user(self):
        client.login(username="test", password="test")
        response = client.post(
            reverse("menu:dishes-list"),
            data=json.dumps(self.valid_dish),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_dish_logged_user(self):
        client.login(username="test", password="test")
        response = client.post(
            reverse("menu:dishes-list"),
            data=json.dumps(self.invalid_dish),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid_dish_not_logged_user(self):
        response = client.put(
            reverse("menu:dishes-detail", kwargs={"pk": self.dish_meat.pk}),
            data=json.dumps(self.valid_dish),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_valid_dish_logged_user(self):
        client.login(username="test", password="test")
        response = client.put(
            reverse("menu:dishes-detail", kwargs={"pk": self.dish_meat.pk}),
            data=json.dumps(self.valid_dish),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_valid_dish_logged_user_not_owner(self):
        client.login(username="test", password="test")
        response = client.put(
            reverse("menu:dishes-detail", kwargs={"pk": self.dish_vege.pk}),
            data=json.dumps(self.valid_dish),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_invalid_dish_logged_user(self):
        client.login(username="test", password="test")
        response = client.put(
            reverse("menu:dishes-detail", kwargs={"pk": self.dish_vege.pk}),
            data=json.dumps(self.invalid_dish),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_dish_not_logged_user(self):
        response = client.delete(
            reverse("menu:dishes-detail", kwargs={"pk": self.dish_meat.pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_dish_logged_user(self):
        client.login(username="test", password="test")
        response = client.delete(
            reverse("menu:dishes-detail", kwargs={"pk": self.dish_meat.pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_dish_logged_user_not_owner(self):
        client.login(username="test", password="test")
        response = client.delete(
            reverse("menu:dishes-detail", kwargs={"pk": self.dish_vege.pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MenuViewSetTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="test"
        )
        self.staff_user = get_user_model().objects.create_user(
            username="test1", password="test1", is_staff=True
        )
        self.dish_meat = Dish.objects.create(
            name="Test Meat Dish 1",
            description="Test meat description 1",
            price="10.50",
            prep_time=60,
            is_vegetarian=False,
            author=self.user,
        )

        self.dish_meat_2 = Dish.objects.create(
            name="Test Meat Dish2",
            description="Test meat description 12",
            price="10.50",
            prep_time=60,
            is_vegetarian=False,
            author=self.user,
        )

        self.menu = Menu.objects.create(
            name="Test Menu 1", description="Test menu description 1", author=self.user
        )
        self.menu.dish.add(self.dish_meat)
        self.menu_staff = Menu.objects.create(
            name="Test Menu 2",
            description="Test menu description 1",
            author=self.staff_user,
        )
        self.menu_staff.dish.add(self.dish_meat)
        self.menu_staff.dish.add(self.dish_meat_2)
        self.valid_menu = {
            "name": "123",
            "description": "123",
            "dish": [self.dish_meat.pk],
        }

        self.invalid_menu = {
            "name": "123" * 1500,
            "description": "123",
            "dish": [self.dish_meat.pk],
        }

    def test_get_all_menus_not_logged_user(self):
        response = client.get(reverse("menu:cards-list"))
        menus = list(Menu.objects.all().order_by("pk"))
        self.assertEqual(response.data[0]["id"], menus[0].pk)
        self.assertEqual(response.data[1]["id"], menus[1].pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_menus_logged_user(self):
        client.login(username="test", password="test")
        response = client.get(reverse("menu:cards-list"))
        menus = list(Menu.objects.all().order_by("pk"))
        self.assertEqual(response.data[0]["id"], menus[0].pk)
        self.assertEqual(response.data[1]["id"], menus[1].pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sort_name_ascending(self):
        response = client.get(reverse("menu:cards-list"), {'ordering': 'name'})
        menus = list(Menu.objects.all().order_by("name"))
        self.assertEqual(response.data[0]["id"], menus[0].pk)
        self.assertEqual(response.data[1]["id"], menus[1].pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sort_name_descending(self):
        response = client.get(reverse("menu:cards-list"), {'ordering': '-name'})
        menus = list(Menu.objects.all().order_by("-name"))
        self.assertEqual(response.data[0]["id"], menus[0].pk)
        self.assertEqual(response.data[1]["id"], menus[1].pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sort_dishes_count_ascending(self):
        response = client.get(reverse("menu:cards-list"), {'ordering': 'dishes_count'})

        self.assertEqual(response.data[0]["id"], self.menu.pk)
        self.assertEqual(response.data[1]["id"], self.menu_staff.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sort_dishes_count_descending(self):
        response = client.get(reverse("menu:cards-list"), {'ordering': '-dishes_count'})

        self.assertEqual(response.data[0]["id"], self.menu_staff.pk)
        self.assertEqual(response.data[1]["id"], self.menu.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_name_empty(self):
        response = client.get(reverse("menu:cards-list"), {'search': 'pawel'})
        print(response.data)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_one_entry(self):
        response = client.get(reverse("menu:cards-list"), {'search': '1'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.menu.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_two_entry(self):
        response = client.get(reverse("menu:cards-list"), {'search': 'Test'})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_created_at_invalid_data(self):
        date_to_search = date.today() + timedelta(days=1)
        response = client.get(reverse("menu:cards-list"), {'created_at__gte': date_to_search})
        self.assertEqual(response.data, {'created_at__gte': [ErrorDetail(string='Enter a valid date/time.', code='invalid')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_created_at_empty_entry(self):
        date_to_search = datetime.now() + timedelta(days=1)
        response = client.get(reverse("menu:cards-list"), {'created_at__gte': date_to_search})
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_invalid_combination_created_at(self):
        date_end = datetime.now() + timedelta(days=1)
        date_start = datetime.now() - timedelta(days=1)
        response = client.get(reverse("menu:cards-list"), {'created_at__gte': date_end, 'created_at__lte': date_start})
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_valid_combination_created_at(self):
        date_end = datetime.now() + timedelta(days=1)
        date_start = datetime.now() - timedelta(days=1)
        response = client.get(reverse("menu:cards-list"), {'created_at__gte': date_start, 'created_at__lte': date_end})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_updated_at_invalid_data(self):
        date_to_search = date.today() + timedelta(days=1)
        response = client.get(reverse("menu:cards-list"), {'updated_at': date_to_search})
        self.assertEqual(response.data, {'updated_at': [ErrorDetail(string='Enter a valid date/time.', code='invalid')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_updated_at_valid_data(self):
        response = client.get(reverse("menu:cards-list"), {'updated_at': self.menu.updated_at})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.menu.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_valid_menu_not_logged_user(self):
        response = client.post(
            reverse("menu:cards-list"),
            data=json.dumps(self.valid_menu),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_valid_menu_logged_user(self):
        client.login(username="test", password="test")
        response = client.post(
            reverse("menu:cards-list"),
            data=json.dumps(self.valid_menu),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_menu_logged_user(self):
        client.login(username="test", password="test")
        response = client.post(
            reverse("menu:cards-list"),
            data=json.dumps(self.invalid_menu),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid_menu_not_logged_user(self):
        response = client.put(
            reverse("menu:cards-detail", kwargs={"pk": self.menu.pk}),
            data=json.dumps(self.valid_menu),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_valid_menu_logged_user(self):
        client.login(username="test", password="test")
        response = client.put(
            reverse("menu:cards-detail", kwargs={"pk": self.menu.pk}),
            data=json.dumps(self.valid_menu),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_valid_menu_logged_user_not_owner(self):
        client.login(username="test", password="test")
        response = client.put(
            reverse("menu:cards-detail", kwargs={"pk": self.menu_staff.pk}),
            data=json.dumps(self.valid_menu),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_invalid_menu_logged_user(self):
        client.login(username="test", password="test")
        response = client.put(
            reverse("menu:cards-detail", kwargs={"pk": self.menu.pk}),
            data=json.dumps(self.invalid_menu),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_menu_not_logged_user(self):
        response = client.delete(
            reverse("menu:cards-detail", kwargs={"pk": self.menu.pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_menu_logged_user(self):
        client.login(username="test", password="test")
        response = client.delete(
            reverse("menu:cards-detail", kwargs={"pk": self.menu.pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_menu_logged_user_not_owner(self):
        client.login(username="test", password="test")
        response = client.delete(
            reverse("menu:cards-detail", kwargs={"pk": self.menu_staff.pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)