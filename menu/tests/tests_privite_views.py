from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from menu.models import Menu, Dish
from menu.views import MenuListView, MenuDetailedView, DishListView, DishDetailedView

factory = APIRequestFactory()
api_client = APIClient()
user = get_user_model()


class MenuListViewTests(APITestCase):
    def setUp(self) -> None:
        self.view_menu = MenuListView
        self.view = MenuListView.as_view()
        self.url = reverse("menu:private_menu")

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


class MenuDetailedViewTest(APITestCase):
    def setUp(self) -> None:
        self.view_menu = MenuDetailedView
        self.view = MenuDetailedView.as_view()
        self.url = reverse("menu:private_menu_detail", kwargs={'pk': 1})

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
        self.assertEqual(self.url, "/v1/private/menu/1")

    def test_unauthorized_get_menu_detail(self):
        response = api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_post_menu_detail(self):
        response = api_client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_put_menu_detail(self):
        response = api_client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_patch_menu_detail(self):
        response = api_client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_menu_detail(self):
        response = api_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_get_menu_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.get(reverse("menu:private_menu_detail", kwargs={'pk': self.menu1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.menu1.id)

    def test_authorized_post_menu_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.post(reverse("menu:private_menu_detail", kwargs={'pk': self.menu1.id}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authorized_put_menu_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.put(reverse("menu:private_menu_detail", kwargs={'pk': self.menu1.id}), data={
            'name': 'Test Menu 1',
            'description': 'PUT',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Menu.objects.filter(id=self.menu1.id).first().description == 'PUT')

    def test_authorized_patch_menu_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.patch(reverse("menu:private_menu_detail", kwargs={'pk': self.menu1.id}), data={
            'description': 'PATCH',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Menu.objects.filter(id=self.menu1.id).first().description == 'PATCH')

    def test_authorized_delete_menu_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.delete(reverse("menu:private_menu_detail", kwargs={'pk': self.menu2.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(id=self.menu2.id))


class DishListViewTests(APITestCase):
    def setUp(self) -> None:
        self.view_menu = DishListView
        self.view = DishListView.as_view()
        self.url = reverse("menu:private_dish")

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
        self.assertEqual(self.url, "/v1/private/dish/")

    def test_get_menu_list_not_authenticated_user(self):
        response = api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_menu_list_authenticated_user(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.dish1.id == response.data[0]['id'])

    def test_post_new_dish(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.post(self.url, data={
            'name': 'Test Meat Dish 13',
            'description': 'Test meat description 1',
            'price': '10.50',
            'prep_time': 60,
            'is_vegetarian': False,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Dish.objects.filter(name="Test Meat Dish 13").first())

    def test_unauthorized_post_new_menu(self):
        response = api_client.post(self.url, data={
            'name': 'Test Meat Dish 14',
            'description': 'Test meat description 1',
            'price': '10.50',
            'prep_time': 60,
            'is_vegetarian': False,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Dish.objects.filter(name="Test Meat Dish 14").first())


class DishDetailedViewTest(APITestCase):
    def setUp(self) -> None:
        self.view_menu = DishDetailedView
        self.view = DishDetailedView.as_view()
        self.url = reverse("menu:private_dish_detail", kwargs={'pk': 1})

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
        self.assertEqual(self.url, "/v1/private/dish/1")

    def test_unauthorized_get_dish_detail(self):
        response = api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_post_dish_detail(self):
        response = api_client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_put_dish_detail(self):
        response = api_client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_patch_dish_detail(self):
        response = api_client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_dish_detail(self):
        response = api_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_get_dish_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.get(reverse("menu:private_dish_detail", kwargs={'pk': self.dish1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.dish1.id)

    def test_authorized_post_dish_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.post(reverse("menu:private_dish_detail", kwargs={'pk': self.dish1.id}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authorized_put_dish_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.put(reverse("menu:private_dish_detail", kwargs={'pk': self.dish1.id}), data={
            'name': 'Test Meat Dish 3',
            'description': 'PUT',
            'price': '10.50',
            'prep_time': 60,
            'is_vegetarian': False,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Dish.objects.filter(id=self.dish1.id).first().description == 'PUT')

    def test_authorized_patch_dish_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.patch(reverse("menu:private_dish_detail", kwargs={'pk': self.dish1.id}), data={
            'description': 'PATCH',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Dish.objects.filter(id=self.dish1.id).first().description == 'PATCH')

    def test_authorized_delete_dish_detail(self):
        api_client.login(username='test_user', password='testpass123')
        response = api_client.delete(reverse("menu:private_dish_detail", kwargs={'pk': self.dish2.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Dish.objects.filter(id=self.dish2.id))
