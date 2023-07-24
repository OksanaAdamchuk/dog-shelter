from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from shelter.models import Caretaker, Dog

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

class CaretakerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Caretaker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email", "expert_level")


class CaretakerUpdateForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Caretaker
        fields = ["username", "first_name", "last_name", "email", "expert_level"]


class BreedSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search by breed name"})
    )


class CaretakerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search by username"})
    )


class DogSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search by dog name"})
    )