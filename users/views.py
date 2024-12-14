from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, UpdateView, DeleteView

from car.forms import CarForm
from .forms import RegistrationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from car.models import Car


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('car:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class MyProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'

    def get(self, request, *args, **kwargs):
        cars = Car.objects.filter(owner=request.user)
        return render(request, self.template_name, {'cars': cars})


class UpdateCarView(LoginRequiredMixin, UpdateView):
    form_class = CarForm
    model = Car  # Specify the model to update
    success_url = reverse_lazy('user:profile')
    template_name = 'update_car.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Car.objects.get(pk=pk)

    def form_valid(self, form):
        # Update the existing car object with the cleaned data
        car = form.save()  # No need for commit=False here
        # No need for additional assignment as form.save() already updates the object
        return super().form_valid(form)


class DeleteCarView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('user:profile')

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        object.delete()
        return redirect('user:profile')
