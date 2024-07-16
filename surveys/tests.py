from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker

from accounts.models import Patient
from doctors.models import Doctor, Speciality


class RateCommentCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.speciality = baker.make(Speciality)
        self.user = User.objects.create_user("test", "test@test.com", "12345678")
        self.patient = baker.make(Patient, user=self.user)
        self.doctor = baker.make(Doctor, speciality=self.speciality)

        self.client.login(username="test", password="12345678")

    def test_rate_comment_create_view_renders_correct_template(self):
        response = self.client.get(reverse("surveys:rate-create", args=[self.doctor.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surveys/rate_comment_create.html")

        response = self.client.get(reverse("surveys:comment-create", args=[self.doctor.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surveys/rate_comment_create.html")

    def test_rate_comment_create_view_returns_404_for_invalid_doctor_pk(self):
        response = self.client.get(reverse("surveys:rate-create", args=[999]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse("surveys:comment-create", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_post_rate_create_form_valid(self):
        response = self.client.post(
            reverse("surveys:rate-create", args=[self.doctor.pk]),
            {"score": 5},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.doctor.rates.filter(score=5).exists())

    def test_post_rate_create_form_invalid(self):
        response = self.client.post(
            reverse("surveys:rate-create", args=[self.doctor.pk]),
            {"score": 0},
        )
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFormError(form, "score", "Ensure this value is greater than or equal to 1.")

    def test_post_comment_create_form_valid(self):
        response = self.client.post(
            reverse("surveys:comment-create", args=[self.doctor.pk]),
            {"title": "Test title", "content": "Test content"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.doctor.comments.filter(title="Test title", content="Test content").exists())

    def test_post_comment_create_form_invalid(self):
        response = self.client.post(reverse("surveys:comment-create", args=[self.doctor.pk]))
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFormError(form, "title", "This field is required.")
        self.assertFormError(form, "content", "This field is required.")

    def test_rate_comment_create_view_redirect_to_doctor_detail(self):
        response = self.client.post(
            reverse("surveys:rate-create", args=[self.doctor.pk]),
            {"score": 5},
        )
        self.assertRedirects(response, self.doctor.get_absolute_url())

        response = self.client.post(
            reverse("surveys:comment-create", args=[self.doctor.pk]),
            {"title": "Test title", "content": "Test content"},
        )
        self.assertRedirects(response, self.doctor.get_absolute_url())
