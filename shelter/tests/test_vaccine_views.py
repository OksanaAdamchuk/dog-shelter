from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from shelter.models import Vaccine


VACCINE_LIST_URL = reverse("shelter:vaccine-list")


class PublicVaccineTests(TestCase):
    def setUp(self) -> None:
        self.vaccine = Vaccine.objects.create(
            name="Test Vaccine",
        )
        self.vaccine1 = Vaccine.objects.create(
            name="Test Vaccine1",
        )

    def test_login_required_to_create_vaccine(self) -> None:
        response = self.client.get(reverse("shelter:vaccine-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_to_update_vaccine(self) -> None:
        response = self.client.get(
            reverse("shelter:vaccine-update", kwargs={"pk": self.vaccine.pk})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_to_delete_vaccine(self) -> None:
        response = self.client.get(
            reverse("shelter:vaccine-delete", kwargs={"pk": self.vaccine.pk})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_retrieve_vaccine_list(self) -> None:
        response = self.client.get(VACCINE_LIST_URL)
        vaccines = Vaccine.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["vaccine_list"]), list(vaccines))
        self.assertTemplateUsed(response, "shelter/vaccine_list.html")


class PrivateVaccineTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password1234@")
        self.client.force_login(self.user)
        super().setUp()

        self.vaccine = Vaccine.objects.create(
            name="Test Vaccine",
        )

    def test_logined_user_has_access_to_create_vaccine(self) -> None:
        response = self.client.get(reverse("shelter:vaccine-create"))

        self.assertEqual(response.status_code, 200)

    def test_logined_user_has_access_to_update_vaccine(self) -> None:
        response = self.client.get(
            reverse("shelter:vaccine-update", kwargs={"pk": self.vaccine.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_logined_user_has_access_to_delete_vaccine(self) -> None:
        response = self.client.get(
            reverse("shelter:vaccine-delete", kwargs={"pk": self.vaccine.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_successful_vaccine_creation(self) -> None:
        data = {
            "name": "New Test Vaccine",
        }
        response = self.client.post(
            reverse("shelter:vaccine-create"), data=data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Vaccine.objects.filter(name="New Test Vaccine").exists())

    def test_unsuccessful_vaccine_creation(self) -> None:
        data = {
            "name": "",
        }
        response = self.client.post(reverse("shelter:vaccine-create"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_create_vaccine_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("shelter:vaccine-create"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/login/?next=/shelter/vaccines/create/"
        )

    def test_redirection_after_vaccine_creation(self) -> None:
        data = {
            "name": "New Test Vaccine",
        }
        response = self.client.post(reverse("shelter:vaccine-create"), data=data)

        self.assertRedirects(response, reverse("shelter:vaccine-list"))

    def test_successful_vaccine_update(self) -> None:
        data = {
            "name": "Updated Test Vaccine",
        }
        response = self.client.post(
            reverse("shelter:vaccine-update", kwargs={"pk": self.vaccine.pk}),
            data=data,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.vaccine.refresh_from_db()
        self.assertEqual(self.vaccine.name, "Updated Test Vaccine")

    def test_unsuccessful_vaccine_update(self) -> None:
        vaccine1 = Vaccine.objects.create(
            name="Old Vaccine",
        )
        data = {
            "name": "",
        }
        response = self.client.post(
            reverse("shelter:vaccine-update", kwargs={"pk": vaccine1.pk}),
            data=data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        vaccine1.refresh_from_db()
        self.assertContains(response, "This field is required.")
        self.assertEqual(vaccine1.name, "Old Vaccine")

    def test_update_vaccine_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(
            reverse("shelter:vaccine-update", kwargs={"pk": self.vaccine.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/login/?next=/shelter/vaccines/1/update/"
        )

    def test_redirection_after_vaccine_update(self) -> None:
        data = {
            "name": "Updated Vaccine",
        }
        response = self.client.post(
            reverse("shelter:vaccine-update", kwargs={"pk": self.vaccine.pk}), data=data
        )

        self.assertRedirects(response, reverse("shelter:vaccine-list"))

    def test_successful_vaccine_deletion(self) -> None:
        vaccine = Vaccine.objects.create(name="Test vaccine")
        response = self.client.post(
            reverse("shelter:vaccine-delete", kwargs={"pk": vaccine.pk}), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Vaccine.objects.filter(pk=vaccine.pk).exists())

    def test_delete_vaccine_anonymous_user_redirect(self) -> None:
        self.client.logout()
        response = self.client.get(
            reverse("shelter:vaccine-delete", kwargs={"pk": self.vaccine.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/login/?next=/shelter/vaccines/1/delete/"
        )

    def test_redirection_after_vaccine_delete(self) -> None:
        vaccine = Vaccine.objects.create(name="Test vaccine")
        response = self.client.post(
            reverse("shelter:vaccine-delete", kwargs={"pk": vaccine.pk}), follow=True
        )

        self.assertRedirects(response, reverse("shelter:vaccine-list"))
