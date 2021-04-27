from datetime import date, timedelta
from unittest.mock import patch, call

from django.contrib.auth import get_user_model
from django.test import TestCase

from config.settings import EMAIL_HOST_USER
from menu.utils import send_email, send_update_email


class SendEmailTest(TestCase):
    def setUp(self) -> None:
        self.receiver = "receiver@email.com"
        self.title = "title"
        self.message = "Testing msg"

    @patch("menu.utils.send_mail")
    def test_send_email_return_error(self, mock_send_email):
        mock_send_email.return_value = 2
        with self.assertLogs() as captured:
            send_email(self.receiver, self.title, self.message)
        self.assertEqual(
            captured.records[0].getMessage(), f"Could not send email {self.receiver}"
        )

    @patch("menu.utils.send_mail")
    def test_send_email_successfully(self, mock_send_email):
        mock_send_email.return_value = 1

        send_email(self.receiver, self.title, self.message)

        mock_send_email.assert_called_once()
        mock_send_email.assert_called_with(
            "title",
            None,
            EMAIL_HOST_USER,
            ["receiver@email.com"],
            html_message="Testing msg",
        )


class SendUpdateEmail(TestCase):
    def setUp(self) -> None:
        self.empty_msg = '<!doctype html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport"\n          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">\n    <meta http-equiv="X-UA-Compatible" content="ie=edge">\n    <title>Dishes update from April 26, 2021</title>\n</head>\n<body>\n<h1>Dishes update from April 26, 2021 </h1>\n\n    <h2> No new or updated dishes </h2>\n\n\n</body>\n</html>\n'
        self.date = date.today()

    @patch("menu.utils.send_email")
    def test_no_receiver(self, mock_send_email):
        send_update_email()
        mock_send_email.assert_not_called()

    @patch("menu.utils.send_email")
    def test_one_receiver(self, mock_send_email):
        get_user_model().objects.create(username="Adam", email="test@wp.pl")
        send_update_email()
        mock_send_email.assert_called_once()
        mock_send_email.assert_called_with(
            "test@wp.pl", f"Update on {self.date}", self.empty_msg
        )

    @patch("menu.utils.send_email")
    def test_two_receiver(self, mock_send_email):
        get_user_model().objects.create(username="Adam", email="test@wp.pl")
        get_user_model().objects.create(username="Adam2", email="test2@wp.pl")

        send_update_email()

        self.assertEqual(mock_send_email.call_count, 2)
        mock_send_email.assert_has_calls(
            [
                call("test@wp.pl", f"Update on {self.date}", self.empty_msg),
                call("test2@wp.pl", f"Update on {self.date}", self.empty_msg),
            ]
        )