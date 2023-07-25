from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from shelter.models import Breed


CARETAKER_LIST_URL = reverse("shelter:caretaker-list")

class PublicCaretakerTests(TestCase):
    def setUp(self) -> None:
        self.caretaker = get_user_model().objects.create_user(
            "test",
            "password1234"
        )

    def test_login_required_caretaker_list(self) -> None:
        response = self.client.get(CARETAKER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_caretaker_detail(self) -> None:
        response = self.client.get(reverse("shelter:caretaker-detail", kwargs={"pk": self.caretaker.pk}))

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_to_update_caretaker(self) -> None:
        response = self.client.get(reverse("shelter:caretaker-update", kwargs={"pk": self.caretaker.pk}))

        self.assertNotEqual(response.status_code, 200)
    
    def test_login_required_to_delete_caretaker(self) -> None:
        response = self.client.get(reverse("shelter:caretaker-delete", kwargs={"pk": self.caretaker.pk}))

        self.assertNotEqual(response.status_code, 200)

    def test_successful_caretaker_creation(self) -> None:
        data = {
            "username": "Test1",
            "password1": "Password1234@",
            "password2": "Password1234@",
            "first_name": "FirstName",
            "last_name": "LastName",
            "expert_level": "beginner"
        }
        response = self.client.post(reverse("shelter:caretaker-create"), data=data, follow=True)
        new_user = get_user_model().objects.get(username=data["username"])

        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user_model().objects.filter(username="Test1").exists())
        self.assertEqual(new_user.first_name, data["first_name"])
        self.assertEqual(new_user.last_name, data["last_name"])
        self.assertEqual(new_user.expert_level, data["expert_level"])

    def test_unsuccessful_caretaker_creation(self) -> None:
        data = {
            "username": "",
            "password1": "Password1234@",
            "password2": "Password1234@",
            "first_name": "FirstName",
            "last_name": "LastName",
            "expert_level": "beginner"
        }
        response = self.client.post(reverse("shelter:caretaker-create"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_redirection_after_caretaker_creation(self) -> None:
        data = {
            "username": "Test1",
            "password1": "Password1234@",
            "password2": "Password1234@",
            "first_name": "FirstName",
            "last_name": "LastName",
            "expert_level": "beginner"
        }
        response = self.client.post(reverse("shelter:caretaker-create"), data=data, follow=True)
        user = get_user_model().objects.get(username="Test1")
        self.client.login(username="Test1", password="Password1234@")
        response = self.client.get(reverse("shelter:caretaker-detail", args=[user.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FirstName")
        self.assertContains(response, "LastName")
        self.assertContains(response, "beginner")


class PrivatecaretakerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234@"
        )
        self.client.force_login(self.user)
        super().setUp()

    def test_logined_user_has_access_to_caretaker_list(self) -> None:
        response = self.client.get(reverse("shelter:caretaker-list"))

        self.assertEqual(response.status_code, 200)

    def test_logined_user_has_access_to_detail_caretaker(self) -> None:
        response = self.client.get(reverse("shelter:caretaker-detail", kwargs={"pk": self.user.pk}))

        self.assertEqual(response.status_code, 200)

    def test_logined_user_has_access_to_update_caretaker(self) -> None:
        response = self.client.get(reverse("shelter:caretaker-update", kwargs={"pk": self.user.pk}))

        self.assertEqual(response.status_code, 200)
    
    def test_logined_user_has_access_to_delete_caretaker(self) -> None:
        response = self.client.get(reverse("shelter:caretaker-delete", kwargs={"pk": self.user.pk}))

        self.assertEqual(response.status_code, 200)

    def test_retrieve_caretaker_list(self) -> None:
        get_user_model().objects.create_user(
            username="Test1", password="Test12345", expert_level="beginner"
        )
        get_user_model().objects.create_user(
            username="Test2", password="Test12345", expert_level="beginner"
        )
        response = self.client.get(CARETAKER_LIST_URL)
        caretakers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["caretaker_list"]), list(caretakers))
        self.assertTemplateUsed(response, "shelter/caretaker_list.html")

    def test_caretaker_list_pagination_is_15(self) -> None:
        number_of_caretakers = 17

        for caretaker_id in range(number_of_caretakers):
            get_user_model().objects.create_user(
                username=f"Dominique {caretaker_id}",
                last_name=f"Surname {caretaker_id}",
                expert_level="beginner",
            )
        response = self.client.get(CARETAKER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["caretaker_list"]), 15)

    def test_lists_all_caretakers_next_page(self) -> None:
        number_of_caretakers = 17

        for caretaker_id in range(number_of_caretakers):
            get_user_model().objects.create_user(
                username=f"Dominique {caretaker_id}",
                last_name=f"Surname {caretaker_id}",
                expert_level="beginner",
            )
        response = self.client.get(CARETAKER_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["caretaker_list"]), 3)

    def test_caretaker_list_with_search_parameter(self) -> None:
        response = self.client.get(CARETAKER_LIST_URL, {"username": "es"})
        caretakers = get_user_model().objects.filter(username__contains="es")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["caretaker_list"]), list(caretakers))

    def test_detail_caretaker_page_context(self) -> None:
        response = self.client.get(reverse("shelter:caretaker-detail", kwargs={"pk": self.user.pk}))
        caretaker_test = get_user_model().objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["caretaker"], caretaker_test)
        self.assertTemplateUsed(response, "shelter/caretaker_detail.html")

    def test_successful_caretaker_update(self) -> None:
        data = {
            "username": "UpdatedUser",
            "first_name": "FirstName",
            "last_name": "LastName",
            "expert_level": "intermediate"
        }
        response = self.client.post(reverse("shelter:caretaker-update", kwargs={"pk": self.user.pk}), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "UpdatedUser")
        self.assertEqual(self.user.expert_level, "intermediate")

    def test_unsuccessful_caretaker_update(self) -> None:
        data = {
            "username": "",
            "first_name": "FirstName",
            "last_name": "LastName",
            "expert_level": "intermediate"
        }
        response = self.client.post(reverse("shelter:caretaker-update", kwargs={"pk": self.user.pk}), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertContains(response, "This field is required.")
        self.assertEqual(self.user.username, "test")

    def test_update_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("shelter:caretaker-update", kwargs={"pk": self.user.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/shelter/caretakers/1/update/")

    def test_redirection_after_caretaker_update(self) -> None:
        data = {
            "username": "UpdatedUser",
            "first_name": "FirstName",
            "last_name": "LastName",
            "expert_level": "intermediate"
        }
        response = self.client.post(reverse("shelter:caretaker-update", kwargs={"pk": self.user.pk}), data=data, follow=True)

        caretaker = get_user_model().objects.get(username="UpdatedUser")
        self.assertRedirects(response, caretaker.get_absolute_url())

    def test_successful_caretaker_deletion(self) -> None:
        caretaker1 = get_user_model().objects.create_user(
            "Caretaker1",
            "password1234@"
        )
        response = self.client.post(reverse("shelter:caretaker-delete", kwargs={"pk": caretaker1.pk}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(pk=caretaker1.pk).exists())

    def test_delete_caretaker_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("shelter:caretaker-delete", kwargs={"pk": self.user.pk}))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/shelter/caretakers/1/delete/")

    def test_redirection_after_caretaker_delete(self) -> None:
        caretaker1 = get_user_model().objects.create_user(
            "Caretaker1",
            "password1234@"
        )
        response = self.client.post(reverse("shelter:caretaker-delete", kwargs={"pk": caretaker1.pk}), follow=True)

        self.assertRedirects(response, reverse("shelter:caretaker-list"))
