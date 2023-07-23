from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from shelter.models import Breed, Caretaker, Dog, Vaccination, Vaccine

def index(request) -> HttpResponse:
    number_of_dogs = Dog.objects.count()
    context = {
        "number_of_dogs": number_of_dogs
    }
    return render(
        request,
        "shelter/index.html",
        context=context
    )


class BreedListView(generic.ListView):
    model = Breed
    paginate_by = 15
    context_object_name = "breed_list"
    queryset = Breed.objects.prefetch_related("dogs")


class BreedDetailView(generic.DetailView):
    model = Breed
    queryset = Breed.objects.prefetch_related("dogs")


class VaccineListView(generic.ListView):
    model = Vaccine
    context_object_name = "vaccine_list"


class DogListView(generic.ListView):
    model = Dog
    context_object_name = "dog_list"
    paginate_by = 10
    queryset = Dog.objects.select_related("breed")


class DogDetailView(generic.DetailView):
    model = Dog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog = self.object
        vaccinations = Vaccination.objects.filter(dog=dog)
        context["vaccinations"] = vaccinations
        return context
    

class CaretakerListView(LoginRequiredMixin, generic.ListView):
    model = Caretaker
    paginate_by = 15
    context_object_name = "caretaker_list"


class CaretakerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Caretaker
    