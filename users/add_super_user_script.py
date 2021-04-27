import os

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('<dependency>', '<dependency>')
    ]

    @staticmethod
    def generate_superuser(apps, schema_editor):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME')
        DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL')
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD')

        superuser = User.objects.create_superuser(
            username=DJANGO_SU_NAME,
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD
        )

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser)
    ]