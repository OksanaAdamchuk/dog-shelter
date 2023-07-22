from django.urls import path

from shelter.views import  BreedDetailView, BreedListView, DogDetailView, DogListView, VaccineListView, index

urlpatterns = [
    path("", index, name="index"),
    path("breeds/", BreedListView.as_view(), name="breed-list"),
    path(
        "breeds/<int:pk>/", BreedDetailView.as_view(), name="breed-detail"
    ),
    path(
        "vaccines/", VaccineListView.as_view(), name="vaccine-list"
    ),
    path(
        "dogs/", DogListView.as_view(), name="dog-list"
    ),
    path(
        "dogs/<int:pk>/", DogDetailView.as_view(), name="dog-detail"
    )
]

app_name = "shelter"