from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegisterForm


class AccountViewTestCase(TestCase):
    def setUp(self):

        self.user_data = {
            "username": "testuser",
            "password1": "djangoP@ssw0rd",
            "password2": "djangoP@ssw0rd",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "093012345678",
            "birth_date": "2000-01-01",
            "address": "Addres1 city 1 ",
        }

    def test_register_view_get(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertIsInstance(response.context["form"], RegisterForm)

    def test_register_view_post_success(self):
        response = self.client.post(reverse("accounts:register"), self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_view_post_fail(self):
        user_data_fail = self.user_data.copy()
        user_data_fail["phone_number"] = "12563"
        response = self.client.post(reverse("accounts:register"), user_data_fail)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(patient__phone_number="12563").exists())
        self.assertFormError(response, "form", "phone_number", "Enter a valid phone number")
