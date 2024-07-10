from django.test import TestCase, RequestFactory
from django.urls import reverse
from model_bakery import baker

from doctors.models import Doctor, Speciality


class IndexHomePageViewTestCase(TestCase):
    """
    Test case for the IndexHomePageView.
    """

    def setUp(self):
        """
        Set up some doctors and a request factory for testing.
        """
        # Create some doctors for testing
        self.speciality1 = Speciality.objects.create(name="TestSpeciality1")
        self.speciality2 = Speciality.objects.create(name="TestSpeciality2")
        self.doctor1 = baker.make(Doctor, speciality=self.speciality1)
        self.doctor2 = baker.make(Doctor, speciality=self.speciality2)
        self.doctor3 = baker.make(Doctor, speciality=self.speciality1)
        self.doctor4 = baker.make(Doctor, speciality=self.speciality2)
        # Create a request factory for testing
        self.factory = RequestFactory()

    def test_get_context_data_no_speciality_filter(self):
        """
        Test the get_context_data method when no speciality filter is provided.
        """
        response = self.client.get(reverse("home:index"))

        self.assertEqual(response.status_code, 200)

        context = response.context_data
        self.assertEqual(len(context["doctors"]), 4)  # There are 4 doctors in the queryset
        self.assertNotIn("speciality_filter", context)  # No speciality filter is provided

    def test_get_context_data_empty_speciality_filter(self):
        """
        Test the get_context_data method when an empty speciality filter is provided.
        """
        response = self.client.get(reverse("home:index"), {"speciality": ""})

        self.assertEqual(response.status_code, 200)

        context = response.context_data
        self.assertEqual(len(context["doctors"]), 4)  # There are 4 doctors in the queryset
        self.assertNotIn("speciality_filter", context)  # No speciality filter is provided

    def test_get_context_data_non_existent_speciality(self):
        """
        Test the get_context_data method when a non-existent speciality filter is provided.
        """
        response = self.client.get(reverse("home:index"), {"speciality": "NonExistentSpeciality"})
        self.assertEqual(response.status_code, 200)

        # Assert that the context contains the expected data
        context = response.context_data
        self.assertEqual(len(context["doctors"]), 0)  # There are no doctors with the given speciality
        self.assertNotIn("speciality_filter", context)  # No speciality filter is provided

    def test_get_context_data_with_speciality_filter(self):
        """
        Test the get_context_data method when a valid speciality filter is provided.
        """
        # Create a request with a speciality filter
        response = self.client.get(reverse("home:index"), {"speciality": "TestSpeciality1"})

        self.assertEqual(response.status_code, 200)

        context = response.context_data
        self.assertEqual(len(context["doctors"]), 2)  # There are 2 doctors with the given speciality
        self.assertEqual(context["speciality_filter"], "TestSpeciality1")  # The speciality filter is provided

    def test_get_context_data_with_uppercase_speciality_filter(self):
        """
        Test the get_context_data method when a valid speciality filter (in uppercase) is provided.
        """
        # Create a request with a speciality filter in uppercase
        response = self.client.get(reverse("home:index"), {"speciality": "TESTSPECIALITY1"})

        # Assert that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the context contains the expected data
        context = response.context_data
        self.assertEqual(len(context["doctors"]), 2)  # There are 2 doctors with the given speciality
        self.assertEqual(context["speciality_filter"], "TESTSPECIALITY1")  # The speciality filter is provided
