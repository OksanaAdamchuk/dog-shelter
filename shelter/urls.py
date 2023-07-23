from django.urls import path

from shelter.views import (
    BreedCreateView,
    BreedDeleteView,
    BreedDetailView,
    BreedListView,
    BreedUpdateView,
    CaretakerDetailView,
    CaretakerListView,
    DogDetailView,
    DogListView,
    VaccineListView,
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
        "dogs/", DogListView.as_view(), name="dog-list"
    ),
    path(
        "dogs/<int:pk>/", DogDetailView.as_view(), name="dog-detail"
    ),
    path(
        "caretakers/", CaretakerListView.as_view(), name="caretaker-list"
    ),
    path(
        "caretakers/<int:pk>/", CaretakerDetailView.as_view(), name="caretaker-detail"
    ),
    
]

app_name = "shelter"