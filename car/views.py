from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Manufacturer, Model, CarGeneration, Car


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the filter parameters from the request
        car_name = self.request.GET.get('car_name')
        car_manufacturer = self.request.GET.get('car_manufacturer')
        car_model = self.request.GET.get('car_model')
        car_generation = self.request.GET.get('car_generation')

        cars = Car.objects.all()

        if car_name:
            cars = cars.filter(name__icontains=car_name)
        if car_manufacturer:
            cars = cars.filter(model__manufacturer__name__icontains=car_manufacturer)
        if car_model:
            cars = cars.filter(model__name__icontains=car_model)
        if car_generation:
            cars = cars.filter(generation__name__icontains=car_generation)

        manufacturers = Manufacturer.objects.all()
        models = Model.objects.all()
        generations = CarGeneration.objects.all()

        context['cars'] = cars
        context['manufacturers'] = manufacturers
        context['models'] = models
        context['generations'] = generations

        return context