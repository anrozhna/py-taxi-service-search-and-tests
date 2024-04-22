from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.tests.test_views.initial_data import (
    CAR_CREATE_URL,
    CAR_LIST_URL,
    CAR_DELETE_URL,
    CAR_DATA,
    CAR_UPDATE_URL
)
from taxi.models import Manufacturer, Car


class CarChangesViewTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",
        )

        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

        self.car.drivers.add(self.user)

        self.client.force_login(self.user)

    def test_successful_car_creation(self):
        response = self.client.post(CAR_CREATE_URL, data={
            "model": "test",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        })
        print(response)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Car.objects.filter(id=2).exists()
        )
        self.assertRedirects(response, CAR_LIST_URL)

    def test_unsuccessful_car_creation(self):
        response = self.client.post(CAR_CREATE_URL, data=CAR_DATA)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Car.objects.filter(model="test").exists()
        )

    def test_car_update_redirects_to_success_url(self):
        response = self.client.post(CAR_UPDATE_URL, data={
            "model": "test",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        })
        self.assertRedirects(response, CAR_LIST_URL)

    def test_car_successful_deletion_redirects_to_success_url(self):
        response = self.client.post(CAR_DELETE_URL)
        self.assertRedirects(response, CAR_LIST_URL)

    def test_successful_deletion_removes_car_from_database(self):
        self.client.post(CAR_DELETE_URL)
        self.assertFalse(Car.objects.filter(
            pk=self.car.pk
        ).exists())