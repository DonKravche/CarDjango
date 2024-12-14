from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, FormView

from .models import Manufacturer, Model, CarGeneration, Car
from .forms import CarForm
from django.urls.base import reverse_lazy

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sale_type = self.request.GET.get('sale_type')
        manufacturer = self.request.GET.get('manufacturer')
        generation = self.request.GET.get('generation')
        year = self.request.GET.get('year')
        fuel_type = self.request.GET.get('fuel_type')

        cars = Car.objects.all()
        # _____________________
        cars = cars.order_by('id')

        if sale_type == 'rent':
            cars = cars.filter(sale_type='rent')
        elif sale_type == 'sale':
            cars = cars.filter(sale_type='sale')

        if manufacturer:
            cars = cars.filter(model__manufacturer__name=manufacturer)
        if generation:
            cars = cars.filter(generation__name=generation)
        if year:
            cars = cars.filter(year=year)
        if fuel_type:
            cars = cars.filter(fuel_type=fuel_type)

        search_query = self.request.GET.get('q')

        if search_query:
            cars = cars.filter(
                Q(model__manufacturer__name__icontains=search_query) |
                Q(model__name__icontains=search_query) |
                Q(name__icontains=search_query)
            )

        paginator = Paginator(cars, 6)
        page_number = self.request.GET.get('page')

        try:
            cars_page = paginator.page(page_number)
        except PageNotAnInteger:
            cars_page = paginator.page(1)
        except EmptyPage:
            cars_page = paginator.page(paginator.num_pages)

        context['cars'] = cars_page
        context['manufacturers'] = Manufacturer.objects.all()
        context['models'] = Model.objects.all().prefetch_related('car_generation')
        context['years'] = sorted(set(Car.objects.values_list('year', flat=True)))
        context['fuel_types'] = sorted(set(Car.objects.values_list('fuel_type', flat=True)))

        return context


class CarDetailView(DetailView):
    template_name = 'car_detail.html'
    context_object_name = 'car'
    model = Car


class AddCarView(LoginRequiredMixin, FormView):
    form_class = CarForm
    template_name = 'car_add.html'
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        car = form.save(commit=False)
        car.owner = self.request.user
        car.save()

        return super().form_valid(form)


class AboutUsView(LoginRequiredMixin, TemplateView):
    template_name = 'about_us.html'


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'contact.html'
