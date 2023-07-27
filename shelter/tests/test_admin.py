from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from shelter.models import Breed, Dog, Vaccination, Vaccine


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="Password1234@"
        )
        self.client.force_login(self.admin_user)
        self.caretaker = get_user_model().objects.create_user(
            username="First Caretaker",
            password="Mypassword78#",
            expert_level="Advanced",
        )
        self.breed = Breed.objects.create(name="Pekiness", dog_size="small")
        self.dog = Dog.objects.create(
            name="Brovko", date_registered="2023-06-20", gender="male", breed=self.breed
        )
        self.vaccine = Vaccine.objects.create(name="Flue")
        self.vaccination = Vaccination.objects.create(
            dog=self.dog, vaccine=self.vaccine, vaccination_date="2023-06-30"
        )

    def test_caretaker_expert_level_listed_on_detail_page(self) -> None:
        url = reverse("admin:shelter_caretaker_change", args=[self.caretaker.id])
        response = self.client.get(url)
        self.assertContains(response, self.caretaker.expert_level)

    def test_breed_dog_size_listed(self) -> None:
        url = reverse("admin:shelter_breed_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.breed.dog_size)

    def test_dog_name_listed(self) -> None:
        url = reverse("admin:shelter_dog_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.dog.name)

    def test_dog_breed_listed(self) -> None:
        url = reverse("admin:shelter_dog_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.dog.breed)

    def test_vaccination_vaccine_listed(self) -> None:
        url = reverse("admin:shelter_vaccination_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.vaccination.vaccine)

    def test_vaccination_dog_listed(self) -> None:
        url = reverse("admin:shelter_vaccination_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.vaccination.dog)
