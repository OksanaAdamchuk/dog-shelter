from django.test import TestCase
from django.contrib.auth import get_user_model

from shelter.forms import CaretakerCreationForm, CaretakerUpdateForm


class CaretakerFormsTest(TestCase):
    def test_caretaker_creation_with_expert_level_email_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "Test",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "FirstName",
            "last_name": "LastName",
            "expert_level": "expert",
            "email": "testemail@mail.com"
        }
        form = CaretakerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_caretaker_update_with_expert_level_email_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "Test",
            "first_name": "FirstName",
            "last_name": "LastName",
            "expert_level": "expert",
            "email": "testemail@mail.com",
            "password": None
        }
        form = CaretakerUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    