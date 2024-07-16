from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from .forms import RegisterForm


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password1": "djangoP@ssw0rd",
            "password2": "djangoP@ssw0rd",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "09301234567",
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
        self.assertRedirects(
            response, expected_url=reverse_lazy("accounts:login"), status_code=302, target_status_code=200
        )

    def test_register_view_post_fail(self):
        user_data_fail = self.user_data.copy()
        user_data_fail["phone_number"] = "12563"
        response = self.client.post(reverse("accounts:register"), user_data_fail)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(patient__phone_number="12563").exists())


class CustomLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.factory = RequestFactory()

    def test_login_view_get(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_view_post_success(self):
        response = self.client.post(reverse("accounts:login"), {"username": "testuser", "password": "password123"})
        self.assertRedirects(response, expected_url=reverse("home:index"), status_code=302, target_status_code=200)

    def test_login_view_post_fail(self):
        response = self.client.post(reverse("accounts:login"), {"username": "testuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertFalse(response.context["form"].is_valid())


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_logout(self):
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(response, expected_url="/", status_code=302, target_status_code=200)
        self.assertNotIn("_auth_user_id", self.client.session)
