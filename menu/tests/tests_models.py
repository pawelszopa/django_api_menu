from django.core.exceptions import ValidationError
from django.test import TestCase

from menu.models import *


class MenuTests(TestCase):
    def setUp(self):
        self.empty_menu = Menu()
        self.user = get_user_model().objects.create(username="Adam")

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
        self.menu.dish.add(self.dish_meat)

    def test_menu_instance(self):
        self.assertTrue(isinstance(self.empty_menu, Menu))

    def test_menu_fields_name(self):
        self.assertEqual(
            [*self.empty_menu.__dict__],
            [
                "_state",
                "id",
                "author_id",
                "name",
                "description",
                "created_at",
                "updated_at",
            ],
        )

    def test_menu_creation(self):
        self.assertTrue(isinstance(self.menu, Menu))
        self.assertIsNotNone(self.menu.id)
        self.assertEqual(self.menu.name, "Test Menu 1")
        self.assertEqual(self.menu.description, "Test menu description 1")
        self.assertEqual(self.menu.author, self.user)

    def test_relationship(self):
        self.assertEqual(self.menu.dish.count(), 1)
        self.assertTrue(self.dish_meat in self.menu.dish.all())

    def test_menu_str(self):
        self.assertEqual(str(self.menu), "Test Menu 1")

    def test_author_required(self):
        menu = Menu()
        with self.assertRaises(ValidationError) as exc:
            menu.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(exceptions["author"], ["This field cannot be null."])

    def test_name_required(self):
        menu = Menu(author=self.user)
        with self.assertRaises(ValidationError) as exc:
            menu.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(exceptions["name"], ["This field cannot be blank."])

    def test_description_required(self):
        menu = Menu(author=self.user, name="test")
        with self.assertRaises(ValidationError) as exc:
            menu.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(exceptions["description"], ["This field cannot be blank."])

    def test_create_menu_with_too_long_name(self):
        menu = Menu(
            author=self.user,
            name="x" * 257,
            description="Test menu description 1",
        )
        with self.assertRaises(ValidationError) as exc:
            menu.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(
            exceptions["name"],
            ["Ensure this value has at most 255 characters (it has 257)."],
        )

    def test_create_menu_with_already_existing_name(self):
        menu = Menu(
            author=self.user,
            name="Test Menu 1",
            description="Test menu description 1",
        )
        with self.assertRaises(ValidationError) as exc:
            menu.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(exceptions["name"], ["Menu with this Name already exists."])


class DishTests(TestCase):
    def setUp(self):
        self.empty_dish = Dish()
        self.user = get_user_model().objects.create(username="Adam")

        self.dish_meat = Dish.objects.create(
            name="Test Meat Dish 1",
            description="Test meat description 1",
            price="10.50",
            prep_time=60,
            is_vegetarian=False,
            author=self.user,
        )

    def test_dish_instance(self):
        self.assertTrue(isinstance(self.empty_dish, Dish))

    def test_dish_fields(self):
        self.assertEqual(
            [*self.empty_dish.__dict__],
            [
                "_state",
                "id",
                "author_id",
                "name",
                "description",
                "price",
                "prep_time",
                "created_at",
                "updated_at",
                "is_vegetarian",
                "image",
            ],
        )

    def test_dish_creation(self):
        self.assertTrue(isinstance(self.dish_meat, Dish))
        self.assertIsNotNone(self.dish_meat.id)
        self.assertEqual(self.dish_meat.name, "Test Meat Dish 1")
        self.assertEqual(self.dish_meat.description, "Test meat description 1")
        self.assertEqual(self.dish_meat.author, self.user)
        self.assertEqual(self.dish_meat.prep_time, 60)
        self.assertEqual(self.dish_meat.price.__str__(), "10.50")
        self.assertFalse(self.dish_meat.is_vegetarian)

    def test_dish_str(self):
        self.assertEqual(str(self.dish_meat), "Test Meat Dish 1")

    def test_required_fields(self):
        dish = Dish()
        with self.assertRaises(ValidationError) as exc:
            dish.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(len(exceptions.keys()), 6)
        self.assertEqual(exceptions["author"], ["This field cannot be null."])
        self.assertEqual(exceptions["name"], ["This field cannot be blank."])
        self.assertEqual(exceptions["description"], ["This field cannot be blank."])
        self.assertEqual(exceptions["price"], ["This field cannot be null."])
        self.assertEqual(exceptions["prep_time"], ["This field cannot be null."])
        self.assertEqual(
            exceptions["is_vegetarian"], ["“None” value must be either True or False."]
        )

    def test_create_dish_with_too_long_name(self):
        dish = Dish(
            author=self.user,
            name="x" * 257,
            description="Test meat description 1",
            price="10.50",
            prep_time=60,
            is_vegetarian=False,
        )
        with self.assertRaises(ValidationError) as exc:
            dish.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(
            exceptions["name"],
            ["Ensure this value has at most 255 characters (it has 257)."],
        )

    def test_price_2_decimal_places(self):
        dish = Dish(
            author=self.user,
            name="x" * 256,
            description="Test meat description 1",
            price="10.5050",
            prep_time=60,
            is_vegetarian=False,
        )
        with self.assertRaises(ValidationError) as exc:
            dish.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(
            exceptions["price"],
            ["Ensure that there are no more than 2 decimal places."],
        )

    def test_negative_price(self):
        dish = Dish(
            author=self.user,
            name="x" * 256,
            description="Test meat description 1",
            price="-10.50",
            prep_time=60,
            is_vegetarian=False,
        )
        with self.assertRaises(ValidationError) as exc:
            dish.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(
            exceptions["price"], ["Ensure this value is greater than or equal to 0.01."]
        )

    def test_create_dish_with_to_big_price(self):
        dish = Dish(
            name="Test name",
            description="Test meat description 1",
            price="11110.50",
            prep_time=60,
            is_vegetarian=False,
        )
        with self.assertRaises(ValidationError) as exc:
            dish.full_clean()
        exceptions = dict(exc.exception)
        self.assertEqual(
            exceptions["price"],
            ["Ensure that there are no more than 6 digits in total."],
        )