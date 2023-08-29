from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import Company, Department

from .forms import DepartmentsFormSet

class CompanyDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'company'
    template_name = 'company/company_detail.html'

    def get_object(self, queryset=None):
        return self.request.user.company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Организация'
        if self.object:
            context['departments'] = self.object.departments.all()
        return context


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    context_object_name = 'company'
    fields = '__all__'
    template_name = 'company/company_update.html'
    success_url = reverse_lazy('company')

    def get_object(self, queryset=None):
        return self.request.user.company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Организация'
        context['cancel_url'] = reverse_lazy('company')
        return context


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    context_object_name = 'department'
    template_name = 'company/department_detail.html'
    pk_url_kwarg = 'depatrment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['title'] = self.object.name
        return context
