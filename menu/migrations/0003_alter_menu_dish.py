# Generated by Django 3.2 on 2021-04-19 16:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20210419_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='dish',
            field=models.ManyToManyField(related_name='menu', to='menu.Dish', validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]
