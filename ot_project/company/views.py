from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
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


class CompanyDepartmentsSetUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'company/departments_update.html'
    success_url = reverse_lazy('company')

    def get_object(self, queryset=None):
        return self.request.user.company

    def get_form(self, **kwargs):
        return DepartmentsFormSet(instance=self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.get_object()
        context['title'] = "Структурные подразделения"
        return context


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    context_object_name = 'department'
    template_name = 'company/department_detail.html'
    pk_url_kwarg = 'depatrment_id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        if self.request.user.company != obj.get_owner_company():
            raise PermissionDenied(f"Структурное подразделение не принадлежит организации пользователя")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['title'] = self.object.name
        return context
