from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Breed(models.Model):
    DOG_SIZES = [
        ("S", "small"),
        ("M", "medium"),
        ("L", "large"),
        ("G", "giant"),
    ]
    name = models.CharField(max_length=100, unique=True)
    dog_size = models.CharField(max_length=1, choices=DOG_SIZES, default="M")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

class Vaccine(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name


class Dog(models.Model):
    DOG_GENDERS = [
        ("F", "female"),
        ("M", "male"),
    ]
    name = models.CharField(max_length=60, default="No name")
    age = models.CharField(max_length=100, blank=True, null=True)
    date_registered = models.DateField()
    sterilized = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=DOG_GENDERS)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name="dogs")
    vaccines = models.ManyToManyField(Vaccine, through="Vaccination", related_name="dogs")
    caretakers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dogs")

    class Meta:
        ordering = ["date_registered"]

    def __str__(self) -> str:
        return f"{self.name} ({self.breed}, {self.age})"


class Vaccination(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    vaccination_date = models.DateField()


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

