from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, validators=[MinLengthValidator(1)])
    dish = models.ManyToManyField('Dish', related_name='dish', null=False, blank=False, validators=[MinLengthValidator(1)])
    description = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=1500, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    prep_time = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_vegetarian = models.BooleanField()

    def __str__(self):
        return self.name
