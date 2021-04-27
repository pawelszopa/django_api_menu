from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from menu.models import Dish, Menu
from menu.permissions import IsOwnerOrStaffOrAdminOrReadOnly, IsOwnerOrStaffOrAdmin


class NotLoggedInUser:
    is_staff = False
    is_superuser = False


class IsOwnerOrStaffOrAdminOrReadOnlyTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        self.not_logged_user = NotLoggedInUser()
        self.staff_user = get_user_model().objects.create(
            username="staff", is_staff=True
        )
        self.admin_user = get_user_model().objects.create(
            username="admin", is_superuser=True
        )
        self.user = get_user_model().objects.create(username="normal")

        self.dish_meat = Dish.objects.create(
            name="Test Meat Dish 1",
            description="Test meat description 1",
            price="10.50",
            prep_time=60,
            is_vegetarian=False,
            author=self.user,
        )
        self.menu = Menu.objects.create(
            name="Test Menu 1", description="Test menu description 1", author=self.user
        )
        self.menu_staff = Menu.objects.create(
            name="Test Menu 2",
            description="Test menu description 1",
            author=self.staff_user,
        )

    def test_not_logged_user_get(self):
        request = self.factory.get("/")
        request.user = self.not_logged_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_not_logged_user_post(self):
        request = self.factory.post("/")
        request.user = self.not_logged_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()
        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertFalse(permission)

    def test_not_logged_user_put(self):
        request = self.factory.put("/")
        request.user = self.not_logged_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertFalse(permission)

    def test_not_logged_user_delete(self):
        request = self.factory.delete("/")
        request.user = self.not_logged_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertFalse(permission)

    def test_admin_user_get(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_admin_user_post(self):
        request = self.factory.post("/")
        request.user = self.admin_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()
        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_admin_user_put(self):
        request = self.factory.put("/")
        request.user = self.admin_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_admin_user_delete(self):
        request = self.factory.delete("/")
        request.user = self.admin_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly().has_object_permission(
            request, None, self.menu
        )

        permission = permission_check

        self.assertTrue(permission)

    def test_staff_user_get(self):
        request = self.factory.get("/")
        request.user = self.staff_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_staff_user_post(self):
        request = self.factory.post("/")
        request.user = self.staff_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()
        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_staff_user_put(self):
        request = self.factory.put("/")
        request.user = self.staff_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_staff_user_delete(self):
        request = self.factory.delete("/")
        request.user = self.staff_user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly().has_object_permission(
            request, None, self.menu
        )

        permission = permission_check

        self.assertTrue(permission)

    def test_user_get_his_data(self):
        request = self.factory.get("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_user_post_his_data(self):
        request = self.factory.post("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()
        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_user_put_his_data(self):
        request = self.factory.put("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(request, None, self.menu)

        self.assertTrue(permission)

    def test_user_delete_his_data(self):
        request = self.factory.delete("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly().has_object_permission(
            request, None, self.menu
        )

        permission = permission_check

        self.assertTrue(permission)

    def test_user_get_not_his_data(self):
        request = self.factory.get("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(
            request, None, self.menu_staff
        )

        self.assertTrue(permission)

    def test_user_post_not_his_data(self):
        request = self.factory.post("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()
        permission = permission_check.has_object_permission(
            request, None, self.menu_staff
        )

        self.assertFalse(permission)

    def test_user_put_not_his_data(self):
        request = self.factory.put("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly()

        permission = permission_check.has_object_permission(
            request, None, self.menu_staff
        )

        self.assertFalse(permission)

    def test_user_delete_not_his_data(self):
        request = self.factory.delete("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdminOrReadOnly().has_object_permission(
            request, None, self.menu_staff
        )

        permission = permission_check

        self.assertFalse(permission)


class IsOwnerOrStaffOrAdminTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        self.not_logged_user = NotLoggedInUser()
        self.staff_user = get_user_model().objects.create(
            username="staff", is_staff=True
        )
        self.admin_user = get_user_model().objects.create(
            username="admin", is_superuser=True
        )
        self.user = get_user_model().objects.create(username="normal")

        self.dish_meat = Dish.objects.create(
            name="Test Meat Dish 1",
            description="Test meat description 1",
            price="10.50",
            prep_time=60,
            is_vegetarian=False,
            author=self.user,
        )

        self.dish_staff = Dish.objects.create(
            name="Test Meat Dish 1",
            description="Test meat description 1",
            price="10.50",
            prep_time=60,
            is_vegetarian=False,
            author=self.staff_user,
        )

    def test_not_logged_user_get(self):
        request = self.factory.get("/")
        request.user = self.not_logged_user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertFalse(permission)

    def test_not_logged_user_post(self):
        request = self.factory.post("/")
        request.user = self.not_logged_user
        permission_check = IsOwnerOrStaffOrAdmin()
        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertFalse(permission)

    def test_not_logged_user_put(self):
        request = self.factory.put("/")
        request.user = self.not_logged_user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertFalse(permission)

    def test_not_logged_user_delete(self):
        request = self.factory.delete("/")
        request.user = self.not_logged_user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertFalse(permission)

    def test_admin_user_get(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertTrue(permission)

    def test_admin_user_post(self):
        request = self.factory.post("/")
        request.user = self.admin_user
        permission_check = IsOwnerOrStaffOrAdmin()
        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertTrue(permission)

    def test_admin_user_put(self):
        request = self.factory.put("/")
        request.user = self.admin_user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertTrue(permission)

    def test_admin_user_delete(self):
        request = self.factory.delete("/")
        request.user = self.admin_user
        permission_check = IsOwnerOrStaffOrAdmin().has_object_permission(
            request, None, self.dish_meat
        )

        permission = permission_check

        self.assertTrue(permission)

    def test_staff_user_get(self):
        request = self.factory.get("/")
        request.user = self.staff_user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertTrue(permission)

    def test_staff_user_post(self):
        request = self.factory.post("/")
        request.user = self.staff_user
        permission_check = IsOwnerOrStaffOrAdmin()
        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertTrue(permission)

    def test_staff_user_put(self):
        request = self.factory.put("/")
        request.user = self.staff_user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertTrue(permission)

    def test_staff_user_delete(self):
        request = self.factory.delete("/")
        request.user = self.staff_user
        permission_check = IsOwnerOrStaffOrAdmin().has_object_permission(
            request, None, self.dish_meat
        )

        permission = permission_check

        self.assertTrue(permission)

    def test_user_get_his_data(self):
        request = self.factory.get("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertTrue(permission)

    def test_user_post_his_data(self):
        request = self.factory.post("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdmin()
        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertTrue(permission)

    def test_user_put_his_data(self):
        request = self.factory.put("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_meat
        )

        self.assertTrue(permission)

    def test_user_delete_his_data(self):
        request = self.factory.delete("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdmin().has_object_permission(
            request, None, self.dish_meat
        )

        permission = permission_check

        self.assertTrue(permission)

    def test_user_get_not_his_data(self):
        request = self.factory.get("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_staff
        )

        self.assertFalse(permission)

    def test_user_post_not_his_data(self):
        request = self.factory.post("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdmin()
        permission = permission_check.has_object_permission(
            request, None, self.dish_staff
        )

        self.assertFalse(permission)

    def test_user_put_not_his_data(self):
        request = self.factory.put("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdmin()

        permission = permission_check.has_object_permission(
            request, None, self.dish_staff
        )

        self.assertFalse(permission)

    def test_user_delete_not_his_data(self):
        request = self.factory.delete("/")
        request.user = self.user
        permission_check = IsOwnerOrStaffOrAdmin().has_object_permission(
            request, None, self.dish_staff
        )

        permission = permission_check

        self.assertFalse(permission)