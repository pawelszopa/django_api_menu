from datetime import timedelta, datetime

from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from menu.models import Menu, Dish
from menu.serializers import MenuSerializer
from menu.views import PublicMenuListView

factory = APIRequestFactory()
api_client = APIClient()


class PublicMenuListViewTest(APITestCase):
    def setUp(self) -> None:
        self.view_menu = PublicMenuListView
        self.view = PublicMenuListView.as_view()
        self.url = reverse("menu:public_menu")
        self.request = factory.get(self.url)

    def test_url_revers(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)
        self.assertEqual(self.url, "/v1/public/menu/")

    def test_empty_menu_list(self):
        menu = Menu.objects.all()
        serializer = MenuSerializer(menu, many=True)

        response = self.view(self.request)
        response.render()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_empty_menu_list_without_dish(self):
        menu = Menu.objects.create(
            name='Test Menu 1',
            description='Test menu description 1',
        )

        response = api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_not_empty_menu_list_with_dish(self):
        menu = Menu.objects.create(
            name='Test Menu 1',
            description='Test menu description 1',
        )
        dish = Dish.objects.create(
            name='Test Meat Dish 1',
            description='Test meat description 1',
            price='10.50',
            prep_time=60,
            is_vegetarian=False,
        )
        menu.dish.add(dish)
        response = api_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], menu.id)
        self.assertEqual(response.data[0]['dish'][0]['id'], dish.id)
    #
    # def test_not_empty_multiple_menus_list_with_and_without_dish(self):
    #     menu1 = Menu.objects.create(
    #         name='Test Menu 1',
    #         description='Test menu description 1',
    #     )
    #     dish1 = Dish.objects.create(
    #         name='Test Meat Dish 1',
    #         description='Test meat description 1',
    #         price='10.50',
    #         prep_time=60,
    #         is_vegetarian=False,
    #     )
    #     menu2 = Menu.objects.create(
    #         name='Test Menu 2',
    #         description='Test menu description 1',
    #     )
    #     dish2 = Dish.objects.create(
    #         name='Test Meat Dish 2',
    #         description='Test meat description 1',
    #         price='10.50',
    #         prep_time=60,
    #         is_vegetarian=False,
    #     )
    #     menu3 = Menu.objects.create(
    #         name='Test Menu 3',
    #         description='Test menu description 1',
    #     )
    #     dish3 = Dish.objects.create(
    #         name='Test Meat Dish 3',
    #         description='Test meat description 1',
    #         price='10.50',
    #         prep_time=60,
    #         is_vegetarian=False,
    #     )
    #     menu1.dish.add(dish1)
    #     menu1.dish.add(dish3)
    #     menu2.dish.add(dish2)
    #
    #     response = api_client.get(self.url)
    #     self.assertEqual(response.data[0]['id'], menu1.id)
    #     self.assertEqual(response.data[0]['dish'][0]['id'], dish1.id)
    #     self.assertEqual(response.data[0]['dish'][1]['id'], dish3.id)
    #
    #     self.assertEqual(response.data[1]['id'], menu2.id)
    #     self.assertEqual(response.data[1]['dish'][0]['id'], dish2.id)
    #
    #     with self.assertRaises(IndexError):
    #         self.assertTrue(response.data[2])


class PublicMenuListViewQuerysetTest(APITestCase):
    def setUp(self) -> None:
        self.view_menu = PublicMenuListView
        self.view = PublicMenuListView.as_view()
        self.url = reverse("menu:public_menu")
        self.request = factory.get(self.url)

        self.menu1 = Menu.objects.create(
            name='Test Menu 1',
            description='Test menu description 1',
        )
        self.dish1 = Dish.objects.create(
            name='Test Meat Dish 1',
            description='Test meat description 1',
            price='10.50',
            prep_time=60,
            is_vegetarian=False,
        )
        self.menu2 = Menu.objects.create(
            name='Test Menu 2',
            description='Test menu description 1',

        )
        self.dish2 = Dish.objects.create(
            name='Test Meat Dish 2',
            description='Test meat description 1',
            price='10.50',
            prep_time=60,
            is_vegetarian=False,
        )
        self.menu3 = Menu.objects.create(
            name='Test Menu 3',
            description='Test menu description 1',
        )
        self.dish3 = Dish.objects.create(
            name='Test Meat Dish 3',
            description='Test meat description 1',
            price='10.50',
            prep_time=60,
            is_vegetarian=False,
        )
        self.menu1.dish.add(self.dish1)
        self.menu1.dish.add(self.dish3)
        self.menu2.dish.add(self.dish2)

        self.menu1.updated_at += timedelta(days=5)

    def test_filter_by_name(self):
        response = api_client.get(self.url, {'fn': '2'})

        self.assertEqual(response.data[0]['id'], self.menu2.id)
        self.assertEqual(response.data[0]['dish'][0]['id'], self.dish2.id)

    def test_sort_by_name_asc(self):
        response = api_client.get(self.url, {'sn': 'ASC'})

        self.assertTrue(response.data[0]['name'] == self.menu1.name)
        self.assertTrue(response.data[1]['name'] == self.menu2.name)

        with self.assertRaises(IndexError):
            self.assertTrue(response.data[2]['name'] == self.menu3.name)

    def test_sort_by_name_desc(self):
        response = api_client.get(self.url, {'sn': 'DESC'})
        self.assertTrue(response.data[0]['name'] == self.menu2.name)
        self.assertTrue(response.data[1]['name'] == self.menu1.name)
        self.assertFalse(response.data[0]['name'] == self.menu3.name)
        with self.assertRaises(IndexError):
            self.assertTrue(response.data[2])

    def test_sort_by_dish_asc(self):
        response = api_client.get(self.url, {'sd': 'ASC'})
        self.assertTrue(response.data[0]['name'] == self.menu2.name)
        self.assertTrue(response.data[1]['name'] == self.menu1.name)
        with self.assertRaises(IndexError):
            self.assertTrue(response.data[2])

    def test_sort_by_dish_desc(self):
        response = api_client.get(self.url, {'sd': 'DESC'})
        self.assertTrue(response.data[0]['name'] == self.menu1.name)
        self.assertTrue(response.data[1]['name'] == self.menu2.name)
        with self.assertRaises(IndexError):
            self.assertTrue(response.data[2])

    def test_filter_by_created_gte(self):
        self.menu2.created_at += timedelta(days=5)
        self.menu2.save()
        response = api_client.get(self.url, {'cgte': self.menu1.created_at + timedelta(days=1)})

        self.assertEqual(response.data[0]['id'], self.menu2.id)
        with self.assertRaises(IndexError):
            self.assertTrue(response.data[1])

    def test_filter_by_created_lte(self):
        self.menu2.created_at += timedelta(days=5)
        self.menu2.save()
        response = api_client.get(self.url, {'clte': self.menu1.created_at + timedelta(days=1)})

        self.assertEqual(response.data[0]['id'], self.menu1.id)
        with self.assertRaises(IndexError):
            self.assertTrue(response.data[1])

    def test_filter_by_updated_gte(self):
        date = self.menu1.updated_at - timedelta(days=1)
        menu2 = Menu.objects.filter(id=self.menu2.id).update(updated_at=self.menu2.updated_at + timedelta(days=5))

        response = api_client.get(self.url, {'ugte': date})

        self.assertEqual(response.data[0]['id'], self.menu2.id)
        with self.assertRaises(IndexError):
            self.assertTrue(response.data[1])

    def test_filter_by_updated_lte(self):
        menu2 = Menu.objects.filter(id=self.menu2.id).update(updated_at=self.menu2.updated_at + timedelta(days=5))
        date = self.menu1.updated_at - timedelta(days=1)

        response = api_client.get(self.url, {'ulte': date})

        self.assertEqual(response.data[0]['id'], self.menu1.id)
        with self.assertRaises(IndexError):
            self.assertTrue(response.data[1])
