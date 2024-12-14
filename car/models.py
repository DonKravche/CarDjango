from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Manufacturer(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CarGeneration(models.Model):
    # model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='generations')
    name = models.CharField(max_length=100)  # e.g., "E60", "F10", "G30" for BMW 5 Series

    def __str__(self):
        return f"{self.name}"


class Model(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='models')
    car_generation = models.ManyToManyField(CarGeneration)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"


class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars', null=True, blank=True)
    owner_number = models.CharField(max_length=50, null=True, blank=True)
    SALE_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent')
    ]

    images = models.ImageField(upload_to='uploaded_car_images/', blank=True, null=True)

    name = models.CharField(max_length=100)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='cars')
    generation = models.ForeignKey(
        CarGeneration,
        on_delete=models.CASCADE,
        related_name='cars',
        null=True,
        blank=True
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year)
        ]
    )

    TRANSMISSION_TYPE_CHOICES = [
        ('manual', 'მექანიკა'),
        ('automatic', 'ავტომატიკა'),
        ('tiptronic', 'ტიპტრონიკი'),
        ('variator', 'ვარიატორი')
    ]

    transmission_type = models.CharField(
        max_length=20,
        choices=TRANSMISSION_TYPE_CHOICES,
        null=True,
        blank=True
    )

    description = models.TextField(max_length=500, null=True, blank=True)

    colour = models.CharField(max_length=50)
    doors = models.PositiveSmallIntegerField()

    fuel_type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPE_CHOICES, default='sale')

    def __str__(self):
        generation_str = f" - {self.generation.name}" if self.generation else ""
        return f"{self.model}{generation_str} - {self.year} - {self.sale_type}"
