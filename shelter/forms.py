from django import forms
from django.contrib.auth import get_user_model

from shelter.models import Breed, Caretaker, Dog, Vaccine

class DogForm(forms.ModelForm):
    caretakers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Dog
        fields = [
            "name",
            "age",
            "date_registered",
            "sterilized",
            "gender",
            "breed",
            "caretakers"
        ]