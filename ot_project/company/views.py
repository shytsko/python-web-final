from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from extra_views import InlineFormSetFactory, UpdateWithInlinesView, InlineFormSetView
from .models import Company, Department, DangerousWork, MedicWork, Factor, FactorCondition
from .forms import CompanyHiddenForm, FactorCreateForm, FactorConditionInlineForm


class CompanyOwnerTestMixin(UserPassesTestMixin):
    permission_denied_message = "Объект не принадлежит организации пользователя"

    def test_func(self):
        obj = self.get_object()
        return self.request.user.company == obj.get_owner_company()


class ContextExMixin:
    title = ''
    cancel_url = reverse_lazy('company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['cancel_url'] = self.cancel_url
        context['company'] = self.request.user.company
        return context


class CompanyDetailView(LoginRequiredMixin, ContextExMixin, DetailView):
    context_object_name = 'company'
    template_name = 'company/company_detail.html'
    title = 'Организация'

    def get_object(self, queryset=None):
        return self.request.user.company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['departments'] = self.object.departments.all()
            context['dangerous_works'] = self.object.dangerous_works.all()
            context['medic_works'] = self.object.medic_works.all()
            context['factors'] = self.object.factors.all()
        return context


class CompanyUpdateView(LoginRequiredMixin, ContextExMixin, UpdateView):
    context_object_name = 'company'
    fields = '__all__'
    template_name = 'company/company_update.html'
    success_url = reverse_lazy('company')
    title = 'Организация'

    def get_object(self, queryset=None):
        return self.request.user.company


class CompanyInlinesSetUpdateView(UpdateWithInlinesView):
    model = Company
    form_class = CompanyHiddenForm
    context_object_name = 'company'
    success_url = reverse_lazy('company')

    def get_object(self, queryset=None):
        return self.request.user.company


class DepartmentInline(InlineFormSetFactory):
    model = Department
    fields = '__all__'


class DangerousWorksInline(InlineFormSetFactory):
    model = DangerousWork
    fields = '__all__'


class MedicWorksInline(InlineFormSetFactory):
    model = MedicWork
    fields = '__all__'


class CompanyDepartmentsSetUpdateView(LoginRequiredMixin, ContextExMixin, CompanyInlinesSetUpdateView):
    inlines = (DepartmentInline,)
    template_name = 'company/departments_update.html'
    title = 'Структурные подразделения'


class CompanyDangerousWorksSetUpdateView(LoginRequiredMixin, ContextExMixin, CompanyInlinesSetUpdateView):
    inlines = (DangerousWorksInline,)
    template_name = 'company/dangerous_works_update.html'
    title = 'Работы с повышенной опасность'


class CompanyMedicWorksSetUpdateView(LoginRequiredMixin, ContextExMixin, CompanyInlinesSetUpdateView):
    inlines = (MedicWorksInline,)
    template_name = 'company/medic_works_update.html'
    title = 'Работы, при выполнении которых есть необходимость в профессиональном отборе'


class DepartmentDetailView(LoginRequiredMixin, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = Department
    context_object_name = 'department'
    template_name = 'company/department_detail.html'
    pk_url_kwarg = 'depatrment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class DangerousWorkDetailView(LoginRequiredMixin, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = DangerousWork
    context_object_name = 'work'
    template_name = 'company/dangerous_work_detail.html'
    pk_url_kwarg = 'dangerous_work_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class MedicWorkDetailView(LoginRequiredMixin, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = MedicWork
    context_object_name = 'work'
    template_name = 'company/medic_work_detail.html'
    pk_url_kwarg = 'medic_work_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class FactorDetailView(LoginRequiredMixin, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = Factor
    context_object_name = 'factor'
    template_name = 'company/factor_detail.html'
    pk_url_kwarg = 'factor_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conditions'] = self.object.conditions.all()
        context['title'] = self.object.name
        return context


class FactorCreateView(LoginRequiredMixin, ContextExMixin, CreateView):
    form_class = FactorCreateForm
    template_name = 'company/factor_create.html'
    title = 'Новый производственный фактор'

    def get_initial(self):
        return {'company': self.request.user.company}

    def get_success_url(self):
        return reverse_lazy('factor_update', kwargs={'factor_id': self.object.pk})

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super(FactorCreateView, self).form_valid(form)


class FactorConditionInline(InlineFormSetFactory):
    model = FactorCondition
    fields = '__all__'
    factory_kwargs = {
        'extra': 0,
        'can_delete': False,
        'max_num': 0,
        'form': FactorConditionInlineForm
    }


class FactorUpdateView(LoginRequiredMixin, CompanyOwnerTestMixin, ContextExMixin, UpdateWithInlinesView):
    model = Factor
    context_object_name = 'factor'
    pk_url_kwarg = 'factor_id'
    inlines = (FactorConditionInline,)
    fields = '__all__'
    success_url = reverse_lazy('company')
    template_name = 'company/factor_update.html'
    title = 'Производственный фактор'


class FactorDeleteView(LoginRequiredMixin, CompanyOwnerTestMixin, ContextExMixin, DeleteView):
    model = Factor
    success_url = reverse_lazy('company')
    template_name = 'company/factor_delete_confirm.html'
    pk_url_kwarg = 'factor_id'
    title = 'Удалить фактор'
