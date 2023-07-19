from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from shelter.models import Breed, Caretaker, Dog, Vaccination, Vaccine


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ["name", "dog_size"]
    list_filter = ["dog_size"]
    list_per_page = 10
    search_fields = ["name"]


@admin.register(Caretaker)
class CaretakerAdmin(UserAdmin):
    list_per_page = 10
    list_display = UserAdmin.list_display + ("expert_level", )
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Fields", {
            "fields": ("expert_level",),
            "description": "Choose level from begginer ('I never care about dog before') to "
            "expert ('I have professional experience in taking care of dogs')"
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "expert_level")}),
    )


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ["name", "date_registered", "breed"]
    list_filter = ["date_registered"]
    list_per_page = 10
    search_fields = ["breed__name", "name"]
    list_select_related = ["breed"]



@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ["vaccine", "vaccination_date", "dog"]
    list_per_page = 10
    list_filter = ["vaccination_date"]
    search_fields = ["vaccine__name"]



admin.site.register(Vaccine)
