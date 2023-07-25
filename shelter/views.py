from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from shelter.forms import (
    BreedSearchForm,
    CaretakerCreationForm,
    CaretakerSearchForm,
    CaretakerUpdateForm,
    DogForm,
    DogSearchForm
)

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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(BreedListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = BreedSearchForm(initial={
              "name": name  
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = Breed.objects.prefetch_related("dogs")
        form = BreedSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class BreedDetailView(generic.DetailView):
    model = Breed
    queryset = Breed.objects.prefetch_related("dogs")


class BreedCreateView(LoginRequiredMixin, generic.CreateView):
    model = Breed
    fields = "__all__"
    
    def get_success_url(self):
        return self.object.get_absolute_url()


class BreedUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Breed
    fields = "__all__"

    def get_success_url(self):
        return self.object.get_absolute_url()


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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(DogListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DogSearchForm(initial={
              "name": name  
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = Dog.objects.select_related("breed")
        form = DogSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


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

    def get_success_url(self):
        return self.object.get_absolute_url()


class DogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dog
    form_class = DogForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class DogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dog
    success_url = reverse_lazy("shelter:dog-list")


class CaretakerListView(LoginRequiredMixin, generic.ListView):
    model = Caretaker
    paginate_by = 15
    context_object_name = "caretaker_list"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CaretakerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CaretakerSearchForm(initial={
              "username": username  
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = get_user_model().objects.all()
        form = CaretakerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class CaretakerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Caretaker


class CaretakerCreateView(generic.CreateView):
    model = Caretaker
    form_class = CaretakerCreationForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class CaretakerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Caretaker
    form_class = CaretakerUpdateForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class CaretakerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Caretaker
    success_url = reverse_lazy("shelter:caretaker-list")


class VaccinationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Vaccination
    fields = ["vaccine", "vaccination_date"]
    
    def get_success_url(self):
        dog = self.object.dog

        return dog.get_absolute_url()

    def form_valid(self, form):
        dog_id = self.kwargs["dog_id"]  
        dog = get_object_or_404(Dog, id=dog_id)
        form.instance.dog = dog

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog_id = self.kwargs["dog_id"]
        dog = get_object_or_404(Dog, id=dog_id)
        context["dog"] = dog
        return context


class VaccinationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Vaccination
    fields = ["vaccine", "vaccination_date"]
    
    def get_success_url(self):
        dog = self.object.dog

        return dog.get_absolute_url()

    def form_valid(self, form):
        dog_id = self.kwargs["dog_id"]  
        dog = get_object_or_404(Dog, id=dog_id)
        form.instance.dog = dog

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog_id = self.kwargs["dog_id"]
        dog = get_object_or_404(Dog, id=dog_id)
        context["dog"] = dog
        return context

    def get_queryset(self):
        dog_id = self.kwargs["dog_id"]
        return super().get_queryset().filter(dog_id=dog_id)


class VaccinationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Vaccination
    
    def get_success_url(self):
        dog = self.object.dog

        return dog.get_absolute_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog_id = self.kwargs["dog_id"]
        dog = get_object_or_404(Dog, id=dog_id)
        context["dog"] = dog
        return context
