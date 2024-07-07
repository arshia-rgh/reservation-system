from django.test import TestCase, RequestFactory
from django.urls import reverse

from doctors.models import Doctor, Speciality
from home.views import IndexHomePageView


class IndexHomePageViewTestCase(TestCase):
    def setUp(self):
        # Create some doctors for testing
        self.speciality1 = Speciality.objects.create(name="TestSpeciality1")
        self.speciality2 = Speciality.objects.create(name="TestSpeciality2")
        self.doctor1 = Doctor.objects.create(
            first_name="First Name1",
            last_name="Last Name1",
            speciality=self.speciality1,
            phone_number="09123456789",
            email="test1@test.com",
            address="address1",
            fee=100,
        )
        self.doctor2 = Doctor.objects.create(
            first_name="First Name2",
            last_name="Last Name2",
            speciality=self.speciality2,
            phone_number="09133456789",
            email="test2@test.com",
            address="address2",
            fee=200,
        )
        self.doctor3 = Doctor.objects.create(
            first_name="First Name3",
            last_name="Last Name3",
            speciality=self.speciality1,
            phone_number="09143456789",
            email="test3@test.com",
            address="address3",
            fee=300,
        )
        self.doctor4 = Doctor.objects.create(
            first_name="First Name4",
            last_name="Last Name4",
            speciality=self.speciality2,
            phone_number="09153456789",
            email="test4@test.com",
            address="address4",
            fee=400,
        )

        # Create a request factory for testing
        self.factory = RequestFactory()

    def test_get_context_data_no_speciality_filter(self):
        # Create a request without a speciality filter
        request = self.factory.get(reverse("home:index"))

        # Instantiate the view with the request
        view = IndexHomePageView.as_view()
        response = view(request)

        # Assert that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the context contains the expected data
        context = response.context_data
        self.assertEqual(len(context["doctors"]), 4)  # There are 2 doctors in the queryset
        self.assertNotIn("speciality_filter", context)  # No speciality filter is provided

    def test_get_context_data_empty_speciality_filter(self):
        # Create a request with an empty speciality filter
        request = self.factory.get(reverse("home:index"), {"speciality": ""})

        # Instantiate the view with the request
        view = IndexHomePageView.as_view()
        response = view(request)

        # Assert that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the context contains the expected data
        context = response.context_data
        self.assertEqual(len(context["doctors"]), 4)  # There are 4 doctors in the queryset
        self.assertNotIn("speciality_filter", context)  # No speciality filter is provided

    def test_get_context_data_non_existent_speciality(self):
        # Create a request with a non-existent speciality filter
        request = self.factory.get(reverse("home:index"), {"speciality": "Non-existent Speciality"})

        # Instantiate the view with the request
        view = IndexHomePageView.as_view()
        response = view(request)

        # Assert that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the context contains the expected data
        context = response.context_data
        self.assertEqual(len(context["doctors"]), 0)  # There are no doctors with the given speciality
        self.assertNotIn("speciality_filter", context)  # No speciality filter is provided

    def test_get_context_data_with_speciality_filter(self):
        # Create a request with a speciality filter
        request = self.factory.get(reverse("home:index"), {"speciality": "TestSpeciality1"})

        # Instantiate the view with the request
        view = IndexHomePageView.as_view()
        response = view(request)

        # Assert that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the context contains the expected data
        context = response.context_data
        self.assertEqual(len(context["doctors"]), 2)  # There is 2 doctor with the given speciality
        self.assertEqual(context["speciality_filter"], "TestSpeciality1")  # The speciality filter is provided

    def test_get_context_data_with_uppercase_speciality_filter(self):
        # Create a request with a speciality filter in uppercase
        request = self.factory.get(reverse("home:index"), {"speciality": "TESTSPECIALITY1"})

        # Instantiate the view with the request
        view = IndexHomePageView.as_view()
        response = view(request)

        # Assert that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the context contains the expected data
        context = response.context_data
        self.assertEqual(len(context["doctors"]), 2)  # There is 2 doctor with the given speciality
        self.assertEqual(context["speciality_filter"], "TESTSPECIALITY1")  # The speciality filter is provided
