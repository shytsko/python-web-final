from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from extra_views import InlineFormSetFactory, UpdateWithInlinesView, InlineFormSetView
from .models import Company, Department, DangerousWork, MedicWork, Factor, FactorCondition
from .forms import CompanyHiddenForm


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
            context['dangerous_works'] = self.object.dangerous_works.all()
            context['medic_works'] = self.object.medic_works.all()
            context['factors'] = self.object.factors.all()
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


class CompanyInlinesSetUpdateView(UpdateWithInlinesView):
    model = Company
    form_class = CompanyHiddenForm
    context_object_name = 'company'
    success_url = reverse_lazy('company')
    title = ''

    def get_object(self, queryset=None):
        return self.request.user.company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['cancel_url'] = reverse_lazy('company')
        return context


class DepartmentInline(InlineFormSetFactory):
    model = Department
    fields = ('name',)


class DangerousWorksInline(InlineFormSetFactory):
    model = DangerousWork
    fields = ('name',)


class MedicWorksInline(InlineFormSetFactory):
    model = MedicWork
    fields = ('name', 'punct')


class CompanyDepartmentsSetUpdateView(LoginRequiredMixin, CompanyInlinesSetUpdateView):
    inlines = (DepartmentInline,)
    template_name = 'company/departments_update.html'
    title = 'Структурные подразделения'


class CompanyDangerousWorksSetUpdateView(LoginRequiredMixin, CompanyInlinesSetUpdateView):
    inlines = (DangerousWorksInline,)
    template_name = 'company/dangerous_works_update.html'
    title = 'Работы с повышенной опасность'


class CompanyMedicWorksSetUpdateView(LoginRequiredMixin, CompanyInlinesSetUpdateView):
    inlines = (MedicWorksInline,)
    template_name = 'company/medic_works_update.html'
    title = 'Работы, при выполнении которых есть необходимость в профессиональном отборе'


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    context_object_name = 'department'
    template_name = 'company/department_detail.html'
    pk_url_kwarg = 'depatrment_id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.company != obj.get_owner_company():
            raise PermissionDenied(f"Структурное подразделение не принадлежит организации пользователя")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['title'] = self.object.name
        return context


class DangerousWorkDetailView(LoginRequiredMixin, DetailView):
    model = DangerousWork
    context_object_name = 'work'
    template_name = 'company/dangerous_work_detail.html'
    pk_url_kwarg = 'dangerous_work_id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.company != obj.get_owner_company():
            raise PermissionDenied(f"Объект не принадлежит не принадлежит организации пользователя")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['title'] = self.object.name
        return context


class MedicWorkDetailView(LoginRequiredMixin, DetailView):
    model = MedicWork
    context_object_name = 'work'
    template_name = 'company/medic_work_detail.html'
    pk_url_kwarg = 'medic_work_id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.company != obj.get_owner_company():
            raise PermissionDenied(f"Объект не принадлежит не принадлежит организации пользователя")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['title'] = self.object.name
        return context


class FactorDetailView(LoginRequiredMixin, DetailView):
    model = Factor
    context_object_name = 'factor'
    template_name = 'company/factor_detail.html'
    pk_url_kwarg = 'factor_id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.company != obj.get_owner_company():
            raise PermissionDenied(f"Объект не принадлежит не принадлежит организации пользователя")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conditions'] = self.object.conditions.all()
        context['company'] = self.request.user.company
        context['title'] = self.object.name
        return context
