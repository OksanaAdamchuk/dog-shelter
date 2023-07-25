from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from shelter.models import Breed, Dog


DOG_LIST_URL = reverse("shelter:dog-list")

class PublicDogTests(TestCase):
    def setUp(self) -> None:
        self.breed = Breed.objects.create(
            name="Pekiness",
            dog_size="small"
        )
        self.dog = Dog.objects.create(
            name="Brovko",
            age="7 months",
            date_registered="2023-06-20",
            gender="male",
            breed=self.breed
        )
        self.dog1 = Dog.objects.create(
            name="Fluffy",
            age="7 years",
            date_registered="2023-06-21",
            gender="female",
            breed=self.breed
        )

    def test_login_required_to_create_dog(self) -> None:
        response = self.client.get(reverse("shelter:dog-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_to_update_dog(self) -> None:
        response = self.client.get(reverse("shelter:dog-update", kwargs={"pk": self.dog.pk}))

        self.assertNotEqual(response.status_code, 200)
    
    def test_login_required_to_delete_dog(self) -> None:
        response = self.client.get(reverse("shelter:dog-delete", kwargs={"pk": self.dog.pk}))

        self.assertNotEqual(response.status_code, 200)

    def test_retrieve_dog_list(self) -> None:
        response = self.client.get(DOG_LIST_URL)
        dogs = Dog.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["dog_list"]), list(dogs))
        self.assertTemplateUsed(response, "shelter/dog_list.html")

    def test_dog_list_pagination_is_ten(self) -> None:
        number_of_dogs = 12

        for dog_id in range(number_of_dogs):
            Dog.objects.create(
                name=f"Test Dog {dog_id}",
                age="7 months",
                date_registered="2023-06-20",
                gender="male",
                breed=self.breed
            )
        response = self.client.get(DOG_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["dog_list"]), 10)

    def test_lists_all_dogs_next_page(self) -> None:
        number_of_dogs = 12

        for dog_id in range(number_of_dogs):
            Dog.objects.create(
                name=f"Test Dog {dog_id}",
                age="7 months",
                date_registered="2023-06-20",
                gender="male",
                breed=self.breed
            )
        response = self.client.get(DOG_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["dog_list"]), 4)

    def test_dog_list_with_search_parameter(self) -> None:
        response = self.client.get(DOG_LIST_URL, {"name": "fl"})
        dogs = Dog.objects.filter(name__contains="fl")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["dog_list"]), list(dogs))

    def test_detail_dog_page_context(self) -> None:
        response = self.client.get(reverse("shelter:dog-detail", kwargs={"pk": self.dog.pk}))
        dog_test = Dog.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["dog"], dog_test)
        self.assertTemplateUsed(response, "shelter/dog_detail.html")


class PrivateDogTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234@"
        )
        self.client.force_login(self.user)
        super().setUp()
        self.breed = Breed.objects.create(
            name="Pekiness",
            dog_size="small"
        )

        self.dog = Dog.objects.create(
            name="Brovko",
            age="7 months",
            date_registered="2023-06-20",
            gender="male",
            breed=self.breed
        )

    def test_logined_user_has_access_to_create_dog(self) -> None:
        response = self.client.get(reverse("shelter:dog-create"))

        self.assertEqual(response.status_code, 200)

    def test_logined_user_has_access_to_update_dog(self) -> None:
        response = self.client.get(reverse("shelter:dog-update", kwargs={"pk": self.dog.pk}))

        self.assertEqual(response.status_code, 200)
    
    def test_logined_user_has_access_to_delete_dog(self) -> None:
        response = self.client.get(reverse("shelter:dog-delete", kwargs={"pk": self.dog.pk}))

        self.assertEqual(response.status_code, 200)

    def test_successful_dog_creation(self) -> None:
        data = {
            "name": "Test dog",
            "age": "5 months",
            "date_registered": "2023-06-20",
            "sterilized": True,
            "gender": "male",
            "breed": self.breed.id,
        }
        response = self.client.post(reverse("shelter:dog-create"), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Dog.objects.filter(name="Test dog").exists())

    def test_unsuccessful_dog_creation(self) -> None:
        breed = Breed.objects.create(
            name="Alabai",
            dog_size="giant"
        )
        data = {
            "name": "Test dog",
            "age": "5 months",
            "date_registered": "",
            "gender": "male",
            "breed": breed.id,
        }
        response = self.client.post(reverse("shelter:dog-create"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_create_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("shelter:dog-create"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/shelter/dogs/create/")

    def test_redirection_after_dog_creation(self) -> None:
        breed = Breed.objects.create(
            name="Alabai",
            dog_size="giant"
        )
        data = {
            "name": "Test dog",
            "age": "5 months",
            "date_registered": "2023-06-20",
            "gender": "male",
            "breed": breed.id,
        }
        response = self.client.post(reverse("shelter:dog-create"), data=data, follow=True)

        dog = Dog.objects.get(name="Test dog")
        self.assertRedirects(response, dog.get_absolute_url())

    def test_successful_dog_update(self) -> None:
        breed = Breed.objects.create(
            name="Alabai",
            dog_size="giant"
        )
        data = {
            "name": "Updated dog",
            "age": "5 months",
            "date_registered": "2023-04-20",
            "gender": "male",
            "breed": breed.id,
        }
        response = self.client.post(reverse("shelter:dog-update", kwargs={"pk": self.dog.pk}), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.dog.refresh_from_db()
        self.assertEqual(self.dog.name, "Updated dog")
        expected_date = datetime.strptime("2023-04-20", "%Y-%m-%d").date()
        self.assertEqual(self.dog.date_registered, expected_date)

    def test_unsuccessful_dog_update(self) -> None:
        breed = Breed.objects.create(
            name="Alabai",
            dog_size="giant"
        )
        data = {
            "name": "Updated dog",
            "age": "5 months",
            "date_registered": "2023-04-20",
            "gender": "",
            "breed": breed.id,
        }
        response = self.client.post(reverse("shelter:dog-update", kwargs={"pk": self.dog.pk}), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.dog.refresh_from_db()
        self.assertContains(response, "This field is required.")
        self.assertNotEqual(self.dog.name, "Updated dog")
        self.assertEqual(self.dog.name, "Brovko")
        self.assertEqual(self.dog.gender, "male")

    def test_update_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("shelter:dog-update", kwargs={"pk": self.dog.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/shelter/dogs/1/update/")

    def test_redirection_after_dog_update(self) -> None:
        breed = Breed.objects.create(
            name="Alabai",
            dog_size="giant"
        )
        data = {
            "name": "Updated dog",
            "age": "5 months",
            "date_registered": "2023-04-20",
            "gender": "male",
            "breed": breed.id,
        }
        response = self.client.post(reverse("shelter:dog-update", kwargs={"pk": self.dog.pk}), data=data, follow=True)

        dog = Dog.objects.get(name="Updated dog")
        self.assertRedirects(response, dog.get_absolute_url())

    def test_successful_dog_deletion(self) -> None:
        breed = Breed.objects.create(
            name="Alabai",
            dog_size="giant"
        )
        dog1 = Dog.objects.create(
            name="Brovko1",
            age="7 months",
            date_registered="2023-06-20",
            gender="male",
            breed=breed
        )
        response = self.client.post(reverse("shelter:dog-delete", kwargs={"pk": dog1.pk}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Dog.objects.filter(pk=dog1.pk).exists())

    def test_delete_dog_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("shelter:dog-delete", kwargs={"pk": self.dog.pk}))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/shelter/dogs/1/delete/")

    def test_redirection_after_dog_delete(self) -> None:
        breed = Breed.objects.create(
            name="Alabai",
            dog_size="giant"
        )
        dog1 = Dog.objects.create(
            name="Brovko1",
            age="7 months",
            date_registered="2023-06-20",
            gender="male",
            breed=breed
        )
        response = self.client.post(reverse("shelter:dog-delete", kwargs={"pk": dog1.pk}), follow=True)

        self.assertRedirects(response, reverse("shelter:dog-list"))
