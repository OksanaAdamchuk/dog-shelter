from django.urls import path

from shelter.views import (
    BreedCreateView,
    BreedDeleteView,
    BreedDetailView,
    BreedListView,
    BreedUpdateView,
    CaretakerCreateView,
    CaretakerDeleteView,
    CaretakerDetailView,
    CaretakerListView,
    CaretakerUpdateView,
    DogCreateView,
    DogDeleteView,
    DogDetailView,
    DogListView,
    DogUpdateView,
    VaccineCreateView,
    VaccineDeleteView,
    VaccineUpdateView,
    VaccineListView,
    VaccinationCreateView,
    VaccinationUpdateView,
    index
)

urlpatterns = [
    path("", index, name="index"),
    path("breeds/", BreedListView.as_view(), name="breed-list"),
    path(
        "breeds/<int:pk>/", BreedDetailView.as_view(), name="breed-detail"
    ),
    path(
        "breeds/<int:pk>/update/", BreedUpdateView.as_view(), name="breed-update"
    ),
    path(
        "breeds/<int:pk>/delete/", BreedDeleteView.as_view(), name="breed-delete"
    ),
    path("breeds/create/", BreedCreateView.as_view(), name="breed-create"),
    path(
        "vaccines/", VaccineListView.as_view(), name="vaccine-list"
    ),
    path(
        "vaccines/create/", VaccineCreateView.as_view(), name="vaccine-create"
    ),
    path(
        "vaccines/<int:pk>/update/", VaccineUpdateView.as_view(), name="vaccine-update"
    ),
    path(
        "vaccines/<int:pk>/delete/", VaccineDeleteView.as_view(), name="vaccine-delete"
    ),
    path(
        "dogs/", DogListView.as_view(), name="dog-list"
    ),
    path(
        "dogs/<int:pk>/", DogDetailView.as_view(), name="dog-detail"
    ),
    path(
        "dogs/create/", DogCreateView.as_view(), name="dog-create"
    ),
    path(
        "dogs/<int:pk>/update/", DogUpdateView.as_view(), name="dog-update"
    ),
    path(
        "dogs/<int:pk>/delete/", DogDeleteView.as_view(), name="dog-delete"
    ),
    path(
        "caretakers/", CaretakerListView.as_view(), name="caretaker-list"
    ),
    path(
        "caretakers/<int:pk>/", CaretakerDetailView.as_view(), name="caretaker-detail"
    ),
    path(
        "caretakers/create/", CaretakerCreateView.as_view(), name="caretaker-create"
    ),
    path(
        "caretakers/<int:pk>/update/", CaretakerUpdateView.as_view(), name="caretaker-update"
    ),
    path(
        "caretakers/<int:pk>/delete/", CaretakerDeleteView.as_view(), name="caretaker-delete"
    ),
    path(
        "vaccination/create/<int:dog_id>/", VaccinationCreateView.as_view(), name="vaccination-create"
    ),

]

app_name = "shelter"