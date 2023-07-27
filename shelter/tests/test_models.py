from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from shelter.models import Breed, Dog, Vaccination, Vaccine


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.caretaker = get_user_model().objects.create_user(
            username="First Caretaker",
            first_name="FirstName",
            last_name="LastName",
            password="Mypassword78#",
            expert_level="Advanced",
        )
        self.breed = Breed.objects.create(name="Pekiness", dog_size="small")
        self.dog = Dog.objects.create(
            name="Brovko",
            age="7 months",
            date_registered="2023-06-20",
            gender="male",
            breed=self.breed,
        )
        self.vaccine = Vaccine.objects.create(name="Flue")
        self.vaccination = Vaccination.objects.create(
            dog=self.dog, vaccine=self.vaccine, vaccination_date="2023-06-30"
        )

    def test_breed_str(self) -> None:
        self.assertEqual(str(self.breed), self.breed.name)

    def test_vaccine_str(self) -> None:
        self.assertEqual(str(self.vaccine), self.vaccine.name)

    def test_dog_str(self) -> None:
        self.assertEqual(
            str(self.dog), f"{self.dog.name} ({self.dog.breed}, {self.dog.age})"
        )

    def test_vaccination_str(self) -> None:
        self.assertEqual(
            str(self.vaccination),
            f"{self.vaccination.dog.name} "
            f"({self.vaccination.vaccine.name}, "
            f"{self.vaccination.vaccination_date})",
        )

    def test_caretaker_str(self) -> None:
        self.assertEqual(
            str(self.caretaker),
            (
                f"{self.caretaker.first_name} {self.caretaker.last_name} "
                f"({self.caretaker.username}, expert level: {self.caretaker.expert_level})"
            ),
        )

    def test_breed_get_absolute_url(self) -> None:
        url = self.breed.get_absolute_url()
        expected_url = reverse("shelter:breed-detail", args=[str(self.breed.pk)])

        self.assertEqual(url, expected_url)

    def test_dog_get_absolute_url(self) -> None:
        url = self.dog.get_absolute_url()
        expected_url = reverse("shelter:dog-detail", args=[str(self.dog.pk)])

        self.assertEqual(url, expected_url)

    def test_caretaker_get_absolute_url(self) -> None:
        url = self.caretaker.get_absolute_url()
        expected_url = reverse(
            "shelter:caretaker-detail", args=[str(self.caretaker.pk)]
        )

        self.assertEqual(url, expected_url)
