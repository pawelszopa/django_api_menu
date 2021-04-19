from django.contrib import admin

# Register your models here.
from menu.models import Menu, Dish

admin.site.register(Menu)
admin.site.register(Dish)
