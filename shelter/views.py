from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from shelter.forms import CaretakerCreationForm, DogForm

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


class BreedCreateView(LoginRequiredMixin, generic.CreateView):
    model = Breed
    fields = "__all__"
    success_url = reverse_lazy("shelter:breed-list")


class BreedUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Breed
    fields = "__all__"


class BreedDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Breed
    success_url = reverse_lazy("shelter:breed-list")


class VaccineListView(generic.ListView):
    model = Vaccine
    context_object_name = "vaccine_list"


class VaccineCreateView(LoginRequiredMixin, generic.CreateView):
    model = Vaccine
    fields = "__all__"
    success_url = reverse_lazy("shelter:vaccine-list")


class VaccineUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Vaccine
    fields = "__all__"
    success_url = reverse_lazy("shelter:vaccine-list")


class VaccineDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Vaccine
    success_url = reverse_lazy("shelter:vaccine-list")


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
    

class DogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy("shelter:dog-list")  


class DogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy("shelter:dog-list")


class DogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dog
    success_url = reverse_lazy("shelter:dog-list")


class CaretakerListView(LoginRequiredMixin, generic.ListView):
    model = Caretaker
    paginate_by = 15
    context_object_name = "caretaker_list"


class CaretakerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Caretaker


class CaretakerCreateView(generic.CreateView):
    model = Caretaker
    form_class = CaretakerCreationForm
    success_url = reverse_lazy("shelter:caretaker-list")


class CaretakerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Caretaker
    form_class = CaretakerCreationForm
    success_url = reverse_lazy("shelter:caretaker-list")


class CaretakerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Caretaker
    success_url = reverse_lazy("shelter:caretaker-list")


class VaccinationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Vaccination
    fields = ["vaccine", "vaccination_date"]
    success_url = reverse_lazy("shelter:dog-list")

    def form_valid(self, form):
        dog_id = self.kwargs["dog_id"]  
        dog = get_object_or_404(Dog, id=dog_id)
        form.instance.dog = dog

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog_id = self.kwargs["dog_id"]
        dog = get_object_or_404(Dog, id=dog_id)
        context["dog_id"] = dog_id
        context["dog_name"] = dog.name
        return context
    

class VaccinationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Vaccination
    fields = ["vaccine", "vaccination_date"]
    success_url = reverse_lazy("shelter:dog-list")

    def form_valid(self, form):
        dog_id = self.kwargs["dog_id"]  
        dog = get_object_or_404(Dog, id=dog_id)
        form.instance.dog = dog

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog_id = self.kwargs["dog_id"]
        dog = get_object_or_404(Dog, id=dog_id)
        context["dog_id"] = dog_id
        context["dog_name"] = dog.name
        return context
    
