from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from menu.models import Menu, Dish
from menu.views import MenuListView

factory = APIRequestFactory()
api_client = APIClient()
user = get_user_model()


class MenuListViewTests(APITestCase):
    def setUp(self) -> None:
        self.view_menu = MenuListView
        self.view = MenuListView.as_view()
        self.url = reverse("private_menu")
        self.request = factory.get(self.url)

        self.user = user.objects.create_user(username='test_user', email='test@user.com', password='testpass123')

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

    def test_url_revers(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)
        self.assertEqual(self.url, "/v1/private/menu/")

    def test_get_menu_list_not_authenticated_user(self):
        response = api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_menu_list_authenticated_user(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.menu1.id == response.data[0]['id'])

    def test_post_new_menu(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.post(self.url, data={
            "name": "Test menu 5",
            "description": "Test Menu 5 description"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Menu.objects.filter(name="Test menu 5").first())

    def test_unauthorized_post_new_menu(self):
        response = api_client.post(self.url, data={
            "name": "Test menu 6",
            "description": "Test Menu 6 description"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Menu.objects.filter(name="Test menu 6").first())
