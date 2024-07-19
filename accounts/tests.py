import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone as tz

from .forms import RegisterForm, TransactionForm, UpdatePatientForm
from .models import Patient


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

class WalletViewTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser2",
            "password1": "djangoP@ssw0rd",
            "password2": "djangoP@ssw0rd",
            "email": "test2@example.com",
            "first_name": "Test2",
            "last_name": "User2",
            "phone_number": "09301234566",
            "birth_date": "2003-01-01",
            "address": "Addres2 city 2"
        }
        self.client.post(reverse("accounts:register"), self.user_data)
        self.user = User.objects.get(username="testuser2")
        self.client.login(username="testuser2", password="djangoP@ssw0rd")
        self.patient = Patient.objects.get(user = self.user)
    
    def test_wallet_view_get(self):
        
        response = self.client.get(reverse("accounts:wallet"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("wallet_balance" in response.context)
        self.assertTrue("transaction_form" in response.context)
        self.assertEqual(response.context["wallet_balance"], 0)
        self.assertIsInstance(response.context["transaction_form"], TransactionForm)
        #print(response.context["transaction_form"])

    def test_wallet_view_post(self):

        response = self.client.post(reverse("accounts:wallet"), {"transaction_type":"D", "amount":1000})
        
        self.assertEqual(Patient.objects.get(user=self.user).wallet , 1000)
        self.assertRedirects(response, expected_url="/accounts/wallet/", status_code=302, target_status_code=200)

        response = self.client.post(reverse("accounts:wallet"), data={"transaction_type":"W", "amount":10000})
        self.assertEqual(Patient.objects.get(user=self.user).wallet , 1000)
        self.assertRedirects(response, expected_url="/accounts/wallet/", status_code=302)

        response = self.client.post(reverse("accounts:wallet"), data={"transaction_type":"W", "amount":1000})
        self.assertRedirects(response, expected_url="/accounts/wallet/", status_code=302, target_status_code=200)
        self.assertEqual(Patient.objects.get(user=self.user).wallet , 0)


class TestTransactionForm(TestCase):
    
    def test_empty_form(self):
        form = TransactionForm()
        self.assertIn("amount",form.fields)
        self.assertIn("transaction_type",form.fields)


class TestDashboardView(TestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser3",
            "password1": "djangoP@ssw0rd",
            "password2": "djangoP@ssw0rd",
            "email": "test3@example.com",
            "first_name": "Test3",
            "last_name": "User3",
            "phone_number": "09301234565",
            "birth_date": "1990-11-01",
            "address": "Addres3 city 3"
        }
        self.client.post(reverse("accounts:register"), self.user_data)
        self.user = User.objects.get(username="testuser3")
        self.client.login(username="testuser3", password="djangoP@ssw0rd")
        self.patient = Patient.objects.get(user = self.user)

    def test_dashboard_view_get(self):
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["now"].year, tz.now().year )
        self.assertEqual(response.context["patient"], self.patient )
        app_dict = response.context["appointments"]
        self.assertIn( "not_attended",app_dict )
        self.assertIn( "attended", app_dict )
        self.assertIn("now", response.context)
        self.assertIn(b'<a href="/accounts/profile/">', response.content)
        self.assertIn(b'<a href="/accounts/wallet/">', response.content)

class TestProfileView(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser4",
            "password1": "djangoP@ssw0rd",
            "password2": "djangoP@ssw0rd",
            "email": "test4@example.com",
            "first_name": "Test4",
            "last_name": "User4",
            "phone_number": "09301234564",
            "birth_date": "1994-11-04",
            "address": "Addres4 city 4"
        }
        self.client.post(reverse("accounts:register"), self.user_data)
        self.user = User.objects.get(username="testuser4")
        self.client.login(username="testuser4", password="djangoP@ssw0rd")
        self.patient = Patient.objects.get(user = self.user)

    def test_profile_view_get(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        p_data= response.context["patient_data"]
        self.assertIn("phone_number", p_data)
        self.assertIn("address", p_data)
        self.assertIn("birth_date", p_data)
        self.assertIsInstance(response.context["patient_form"], UpdatePatientForm)
    
    def test_profile_view_post(self):
        data = {"phone_number": "09391311532",
                "address":"round 3 Avenue 4",
                "birth_date": datetime.date(1995, 12 , 6)
                }
        response = self.client.post(reverse("accounts:profile"), data=data)
        self.assertEqual(response.status_code, 200)
        p = Patient.objects.get(user=self.user)
        self.assertEqual(p.phone_number, "09391311532")
        self.assertEqual(p.address, "round 3 Avenue 4")
        self.assertEqual(p.birth_date, datetime.date(1995, 12 , 6))

        data["phone_number"] = "0939131153"
        response = self.client.post(reverse("accounts:profile"), data=data)
        self.assertEqual(response.status_code, 302)
        p = Patient.objects.get(user=self.user)
        self.assertEqual(p.phone_number, "09391311532")
        
        data["birth_date"] = datetime.date(2025, 12 , 6)
        response = self.client.post(reverse("accounts:profile"), data=data)
        self.assertEqual(response.status_code, 302)
        p = Patient.objects.get(user=self.user)
        self.assertEqual(p.phone_number, "09391311532")