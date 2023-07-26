from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from shelter.models import Dog, Breed, Vaccine, Vaccination


class PublicVaccinationTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234@"
        )
        self.breed = Breed.objects.create(name="Alabai", dog_size="medium")
        self.vaccine = Vaccine.objects.create(name="Test Vaccine")
        self.dog = Dog.objects.create(
            name="Test Dog",
            age="2 years",
            date_registered="2023-01-01",
            sterilized=True,
            gender="male",
            breed=self.breed
        )
        self.vaccination = Vaccination.objects.create(
            dog=self.dog,
            vaccine=self.vaccine,
            vaccination_date="2023-07-26"
        )

    def test_login_required_to_create_vaccination(self) -> None:
        response = self.client.get(reverse("shelter:vaccination-create", kwargs={"dog_id": self.dog.id}))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/shelter/vaccination/create/1/")

    def test_login_required_to_update_vaccination(self) -> None:
        response = self.client.get(reverse("shelter:vaccination-update", kwargs={"dog_id": self.dog.id, "pk": self.vaccination.id}))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/shelter/vaccination/update/1/1/")
    
    def test_login_required_to_delete_vaccination(self) -> None:
        response = self.client.get(reverse("shelter:vaccination-delete", kwargs={"dog_id": self.dog.id, "pk": self.vaccination.id}))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/shelter/vaccination/delete/1/1/")


class PrivateVaccinationTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234@"
        )
        self.client.force_login(self.user)
        super().setUp()

        self.breed = Breed.objects.create(name="Alabai", dog_size="medium")
        self.vaccine = Vaccine.objects.create(name="Test Vaccine")
        self.dog = Dog.objects.create(
            name="Test Dog",
            age="2 years",
            date_registered="2023-01-01",
            sterilized=True,
            gender="male",
            breed=self.breed
        )
        self.vaccination = Vaccination.objects.create(
            dog=self.dog,
            vaccine=self.vaccine,
            vaccination_date="2023-07-26"
        )

    def test_successful_vaccination_creation(self) -> None:
        data = {
            "vaccination_date": "2023-07-01",
            "vaccine": self.vaccine.id
        }
        response = self.client.post(reverse("shelter:vaccination-create", kwargs={"dog_id": self.dog.id}), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Vaccination.objects.filter(vaccination_date="2023-07-01").exists())

    def test_unsuccessful_vaccination_creation(self) -> None:
        data = {
            "vaccination_date": "",
            "vaccine": self.vaccine.id
        }
        response = self.client.post(reverse("shelter:vaccination-create", kwargs={"dog_id": self.dog.id}), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_successful_vaccination_update(self) -> None:
        data = {
            "vaccination_date": "2023-07-01",
            "vaccine": self.vaccine.id
        }
        response = self.client.post(reverse("shelter:vaccination-update", kwargs={"dog_id": self.dog.id, "pk": self.vaccination.id}), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.vaccination.refresh_from_db()
        expected_date = datetime.strptime("2023-07-01", "%Y-%m-%d").date()
        self.assertEqual(self.vaccination.vaccination_date, expected_date)

    def test_unsuccessful_vaccination_update(self) -> None:
        data = {
            "vaccination_date": "",
            "vaccine": self.vaccine.id
        }
        response = self.client.post(reverse("shelter:vaccination-update", kwargs={"dog_id": self.dog.id, "pk": self.vaccination.id}), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.vaccination.refresh_from_db()
        self.assertContains(response, "This field is required.")
        expected_date = datetime.strptime("2023-07-26", "%Y-%m-%d").date()
        self.assertEqual(self.vaccination.vaccination_date, expected_date)

    def test_successful_vaccination_deletion(self) -> None:
        vaccination1 = Vaccination.objects.create(
            dog=self.dog,
            vaccine=self.vaccine,
            vaccination_date="2023-06-26"
        )
        response = self.client.post(reverse("shelter:vaccination-delete", kwargs={"dog_id": self.dog.id, "pk": vaccination1.id}))

        self.assertEqual(response.status_code, 302)
        expected_date = datetime.strptime("2023-06-26", "%Y-%m-%d").date()
        self.assertFalse(Vaccination.objects.filter(vaccination_date=expected_date).exists())
