from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from extra_views import InlineFormSetFactory, UpdateWithInlinesView
from .models import Company, Department, DangerousWork, MedicWork, Factor, FactorCondition, Workplace, WorkplaceFactor
from .forms import CompanyHiddenForm, FactorCreateForm, FactorConditionInlineForm, WorkplaceFactorInlineForm, \
    WorkplaceUpdateForm


class LoginRequiredMixinEx(AccessMixin):
    """К действиям стандартного миксина добавлена проверка связи пользователя с организацией"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.permission_denied_message = "Требуется вход"
            return self.handle_no_permission()
        if request.user.company is None:
            self.permission_denied_message = "Текущий пользователь не связан с организацией"
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CompanyOwnerTestMixin:
    """
    Миксин для проверки, связан ли объект с организацией текущего пользователя.
    Класс объекта должен реализовывать метод get_owner_company_id, который возвращает id организации
    """

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.company_id != obj.get_owner_company_id():
            raise PermissionDenied(f"Объект не принадлежит организации пользователя")
        return obj


class ContextExMixin:
    """
    Миксин для объединения часто используемых параметров шаблона
    title - Заголовок страницы, по умолчанию - название организации текущего пользователя
    cancel_url - url для перехода по кнопке "Отмена", по умолчанию - страница организации текущего пользователя
    company - организация текущего пользователя
    """
    title = ''
    cancel_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['title'] = context['company'].name + self.title
        context['cancel_url'] = self.get_cancel_url()
        return context

    def get_cancel_url(self):
        if self.cancel_url:
            return self.cancel_url
        if self.object:
            return self.object.get_absolute_url()
        return reverse_lazy('company')


class CompanyDetailView(LoginRequiredMixinEx, ContextExMixin, DetailView):
    context_object_name = 'company'
    template_name = 'company/company_detail.html'

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


class CompanyUpdateView(LoginRequiredMixinEx, ContextExMixin, UpdateView):
    context_object_name = 'company'
    fields = '__all__'
    template_name = 'company/company_update.html'

    def get_object(self, queryset=None):
        return self.request.user.company


class CompanyInlinesSetUpdateBaseView(UpdateWithInlinesView):
    """
    Базовое представление для редактирования списков объектов, связанных с организацией
    """
    model = Company
    form_class = CompanyHiddenForm
    context_object_name = 'company'

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


class CompanyDepartmentsSetUpdateView(LoginRequiredMixinEx, ContextExMixin, CompanyInlinesSetUpdateBaseView):
    inlines = (DepartmentInline,)
    template_name = 'company/departments_update.html'


class CompanyDangerousWorksSetUpdateView(LoginRequiredMixinEx, ContextExMixin, CompanyInlinesSetUpdateBaseView):
    inlines = (DangerousWorksInline,)
    template_name = 'company/dangerous_works_update.html'


class CompanyMedicWorksSetUpdateView(LoginRequiredMixinEx, ContextExMixin, CompanyInlinesSetUpdateBaseView):
    inlines = (MedicWorksInline,)
    template_name = 'company/medic_works_update.html'


class DepartmentDetailView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = Department
    context_object_name = 'department'
    template_name = 'company/department_detail.html'
    pk_url_kwarg = 'department_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workplaces'] = self.object.workplaces.all()
        return context


class DangerousWorkDetailView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = DangerousWork
    context_object_name = 'work'
    template_name = 'company/dangerous_work_detail.html'
    pk_url_kwarg = 'dangerous_work_id'


class MedicWorkDetailView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = MedicWork
    context_object_name = 'work'
    template_name = 'company/medic_work_detail.html'
    pk_url_kwarg = 'medic_work_id'


class FactorDetailView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = Factor
    context_object_name = 'factor'
    template_name = 'company/factor_detail.html'
    pk_url_kwarg = 'factor_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conditions'] = self.object.conditions.all()
        return context


class FactorCreateView(LoginRequiredMixinEx, ContextExMixin, CreateView):
    form_class = FactorCreateForm
    template_name = 'company/factor_create.html'

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


class FactorUpdateView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, UpdateWithInlinesView):
    model = Factor
    context_object_name = 'factor'
    pk_url_kwarg = 'factor_id'
    inlines = (FactorConditionInline,)
    fields = '__all__'
    template_name = 'company/factor_update.html'


class FactorDeleteView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DeleteView):
    model = Factor
    success_url = reverse_lazy('company')
    template_name = 'company/delete_confirm.html'
    pk_url_kwarg = 'factor_id'


class WorkplaceDetailView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = Workplace
    context_object_name = 'workplace'
    template_name = 'company/workplace_detail.html'
    pk_url_kwarg = 'workplace_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['factors'] = self.object.workplacefactor_set.all()
        context['dangerous_works'] = self.object.dangerous_works.all()
        context['medic_works'] = self.object.medic_works.all()
        return context


class WorkplaceCreateView(LoginRequiredMixinEx, ContextExMixin, CreateView):
    model = Workplace
    fields = ('name', 'extra_description', 'code')
    template_name = 'company/workplace_create.html'

    def get_success_url(self):
        return reverse_lazy('workplace_update', kwargs={'workplace_id': self.object.pk})

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        setattr(self, 'department', get_object_or_404(Department, pk=self.kwargs["department_id"]))

    def get_cancel_url(self):
        return reverse_lazy('department_detail', kwargs={'department_id': self.kwargs["department_id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = self.department
        return context

    def form_valid(self, form):
        form.instance.department = self.department
        return super(WorkplaceCreateView, self).form_valid(form)


class WorkplaceFactorInline(InlineFormSetFactory):
    model = WorkplaceFactor
    fields = '__all__'
    form_class = WorkplaceFactorInlineForm


class WorkplaceUpdateView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, UpdateWithInlinesView):
    model = Workplace
    form_class = WorkplaceUpdateForm
    context_object_name = 'workplace'
    pk_url_kwarg = 'workplace_id'
    inlines = (WorkplaceFactorInline,)
    inlines_names = ('factors',)
    template_name = 'company/workplace_update.html'

    def get_form_class(self):
        form_class = super().get_form_class()
        form_class.company_id = self.request.user.company_id
        return form_class

    def construct_inlines(self):
        inline_formsets = []
        for inline_class in self.get_inlines():
            inline_instance = inline_class(
                self.model, self.request, self.object, self.kwargs, self
            )
            inline_instance.form_class.company_id = self.request.user.company_id
            inline_formset = inline_instance.construct_formset()
            inline_formsets.append(inline_formset)
        return inline_formsets


class WorkplaceDeleteView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DeleteView):
    model = Workplace
    template_name = 'company/delete_confirm.html'
    pk_url_kwarg = 'workplace_id'

    def get_success_url(self):
        return self.object.department.get_absolute_url()
