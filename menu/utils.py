import logging
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import get_template

from config.settings import EMAIL_HOST_USER


def send_email(receiver, title, message):
    mail = send_mail(
        title,
        None,
        EMAIL_HOST_USER,
        [receiver],
        html_message=message
    )
    if mail != 1:
        logging.error(f"Could not send email {receiver}")
    else:
        logging.error(f"Successfully send email to {receiver}")


def send_update_email():
    from menu.models import Dish
    date_to_search = date.today() - timedelta(days=1)
    dishes = Dish.objects.all()
    updated_dishes = dishes.filter(updated_at__date=date_to_search)
    created_dishes = dishes.filter(created_at__date=date_to_search)

    context = {
        "updated_dishes": updated_dishes,
        "created_dishes": created_dishes,
        "date_to_search": date_to_search
    }

    msg = get_template('menu/email.html').render(context)
    title = f"Update on {date.today()}"
    users = get_user_model().objects.all()

    for receiver in users:
        send_email(receiver.email, title, msg)
