from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker

from doctors.models import Doctor, Speciality


class DoctorDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.speciality = Speciality.objects.create(name='Cardiology')
        self.doctor = baker.make(Doctor, speciality=self.speciality, first_name='John', last_name='Doe')

    def test_doctor_detail_view_renders_correct_template(self):
        response = self.client.get(self.doctor.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctors/detail.html')

    def test_doctor_detail_view_contains_expected_doctor_name(self):
        response = self.client.get(self.doctor.get_absolute_url())
        self.assertContains(response, 'John Doe')

    def test_doctor_detail_view_contains_expected_doctor_specialty(self):
        response = self.client.get(self.doctor.get_absolute_url())
        self.assertContains(response, 'Cardiology')

    def test_doctor_detail_view_returns_404_for_invalid_pk(self):
        response = self.client.get(reverse('doctors:detail', args=[999]))
        self.assertEqual(response.status_code, 404)
