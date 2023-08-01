from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from shelter.models import Breed


BREEDS_LIST_URL = reverse("shelter:breed-list")
BREED_CREATE_URL = reverse("shelter:breed-create")


class PublicBreedTests(TestCase):
    def setUp(self) -> None:
        self.breed = Breed.objects.create(name="Pekiness", dog_size="small")
        self.breed1 = Breed.objects.create(name="Alabai", dog_size="giant")

    def test_login_required_to_create_breed(self) -> None:
        response = self.client.get(BREED_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_to_update_breed(self) -> None:
        response = self.client.get(
            reverse("shelter:breed-update", kwargs={"pk": self.breed.pk})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_to_delete_breed(self) -> None:
        response = self.client.get(
            reverse("shelter:breed-delete", kwargs={"pk": self.breed.pk})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_retrieve_breed_list(self) -> None:
        response = self.client.get(BREEDS_LIST_URL)
        breeds = Breed.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["breed_list"]), list(breeds))
        self.assertTemplateUsed(response, "shelter/breed_list.html")

    def test_breed_list_pagination_is_fifteen(self) -> None:
        number_of_breeds = 17

        for breed_id in range(number_of_breeds):
            Breed.objects.create(name=f"DogBreed  {breed_id}", dog_size="small")
        response = self.client.get(BREEDS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["breed_list"]), 15)

    def test_lists_all_breeds_next_page(self) -> None:
        number_of_breeds = 17

        for breed_id in range(number_of_breeds):
            Breed.objects.create(name=f"DogBreed  {breed_id}", dog_size="small")
        response = self.client.get(BREEDS_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["breed_list"]), 4)

    def test_breed_list_with_search_parameter(self) -> None:
        response = self.client.get(BREEDS_LIST_URL, {"name": "pek"})
        breeds = Breed.objects.filter(name__contains="pek")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["breed_list"]), list(breeds))

    def test_detail_breed_page_context(self) -> None:
        response = self.client.get(
            reverse("shelter:breed-detail", kwargs={"pk": self.breed.pk})
        )
        breed_pekines = Breed.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["breed"], breed_pekines)
        self.assertTemplateUsed(response, "shelter/breed_detail.html")


class PrivateBreedTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password1234@")
        self.client.force_login(self.user)
        super().setUp()

        self.breed = Breed.objects.create(name="Pekiness", dog_size="small")

    def test_logined_user_has_access_to_create_breed(self) -> None:
        response = self.client.get(BREED_CREATE_URL)

        self.assertEqual(response.status_code, 200)

    def test_logined_user_has_access_to_update_breed(self) -> None:
        response = self.client.get(
            reverse("shelter:breed-update", kwargs={"pk": self.breed.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_logined_user_has_access_to_delete_breed(self) -> None:
        response = self.client.get(
            reverse("shelter:breed-delete", kwargs={"pk": self.breed.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_successful_breed_creation(self) -> None:
        data = {"name": "Golden Retriever", "dog_size": "medium"}
        response = self.client.post(
            reverse("shelter:breed-create"), data=data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Breed.objects.filter(name="Golden Retriever").exists())

    def test_unsuccessful_breed_creation(self) -> None:
        data = {"name": "", "dog_size": "large"}
        response = self.client.post(reverse("shelter:breed-create"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_create_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("shelter:breed-create"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/shelter/breeds/create/")

    def test_redirection_after_breed_creation(self) -> None:
        data = {"name": "Husky", "dog_size": "large"}
        response = self.client.post(reverse("shelter:breed-create"), data=data)

        breed = Breed.objects.get(name="Husky")
        self.assertRedirects(response, breed.get_absolute_url())

    def test_successful_breed_update(self) -> None:
        data = {"name": "Updated Breed", "dog_size": "large"}
        response = self.client.post(
            reverse("shelter:breed-update", kwargs={"pk": self.breed.pk}),
            data=data,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.breed.refresh_from_db()
        self.assertEqual(self.breed.name, "Updated Breed")
        self.assertEqual(self.breed.dog_size, "large")

    def test_unsuccessful_breed_update(self) -> None:
        breed1 = Breed.objects.create(name="Alabai", dog_size="giant")
        data = {"name": "", "dog_size": "large"}
        response = self.client.post(
            reverse("shelter:breed-update", kwargs={"pk": breed1.pk}),
            data=data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        breed1.refresh_from_db()
        self.assertContains(response, "This field is required.")
        self.assertEqual(breed1.name, "Alabai")
        self.assertEqual(breed1.dog_size, "giant")

    def test_update_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(
            reverse("shelter:breed-update", kwargs={"pk": self.breed.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/login/?next=/shelter/breeds/1/update/"
        )

    def test_redirection_after_breed_update(self) -> None:
        data = {"name": "Husky", "dog_size": "large"}
        response = self.client.post(
            reverse("shelter:breed-update", kwargs={"pk": self.breed.pk}), data=data
        )

        breed = Breed.objects.get(name="Husky")
        self.assertRedirects(response, breed.get_absolute_url())

    def test_successful_breed_deletion(self) -> None:
        breed = Breed.objects.create(name="Test Breed", dog_size="medium")
        response = self.client.post(
            reverse("shelter:breed-delete", kwargs={"pk": breed.pk}), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Breed.objects.filter(pk=breed.pk).exists())

    def test_delete_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(
            reverse("shelter:breed-delete", kwargs={"pk": self.breed.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/login/?next=/shelter/breeds/1/delete/"
        )

    def test_redirection_after_breed_delete(self) -> None:
        breed = Breed.objects.create(name="Test Breed", dog_size="medium")
        response = self.client.post(
            reverse("shelter:breed-delete", kwargs={"pk": breed.pk}), follow=True
        )

        self.assertRedirects(response, reverse("shelter:breed-list"))
