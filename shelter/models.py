from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


class Breed(models.Model):
    DOG_SIZES = [
        ("small", "small"),
        ("medium", "medium"),
        ("large", "large"),
        ("giant", "giant"),
    ]
    name = models.CharField(max_length=100, unique=True)
    dog_size = models.CharField(max_length=10, choices=DOG_SIZES, default="medium")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("shelter:breed-detail", args=[str(self.pk)])
    

class Vaccine(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name


class Dog(models.Model):
    DOG_GENDERS = [
        ("female", "female"),
        ("male", "male"),
    ]
    name = models.CharField(max_length=60, default="No name")
    age = models.CharField(max_length=100, blank=True, null=True)
    date_registered = models.DateField()
    sterilized = models.BooleanField(default=False)
    gender = models.CharField(max_length=6, choices=DOG_GENDERS)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name="dogs")
    vaccines = models.ManyToManyField(Vaccine, through="Vaccination", related_name="dogs")
    caretakers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="dogs", blank=True
    )

    class Meta:
        ordering = ["date_registered"]

    def __str__(self) -> str:
        return f"{self.name} ({self.breed}, {self.age})"
    
    def get_absolute_url(self):
        return reverse("shelter:dog-detail", args=[str(self.pk)])


class Vaccination(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    vaccination_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.dog.name} ({self.vaccine.name}, {self.vaccination_date})"
    


class Caretaker(AbstractUser):
    EXPERT_LEVELS = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    ]
    expert_level = models.CharField(
        max_length=20,
        choices=EXPERT_LEVELS,
        default="beginner"
    )

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name} "
            f"({self.username}, expert level: {self.expert_level})"
        )

    def get_absolute_url(self):
        return reverse("shelter:caretaker-detail", args=[str(self.pk)])