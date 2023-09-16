from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView
from extra_views import InlineFormSetFactory, UpdateWithInlinesView

from company.models import Department
from company.views import CompanyOwnerTestMixin
from home.mixins import ContextExMixin
from user.mixins import LoginRequiredMixinEx
from .forms import WorkplaceFactorInlineForm, WorkplaceUpdateForm
from .models import Workplace, WorkplaceFactor


class WorkplaceDetailView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = Workplace
    context_object_name = 'workplace'
    template_name = 'workplace/workplace_detail.html'
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
    template_name = 'workplace/workplace_create.html'

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
    template_name = 'workplace/workplace_update.html'

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
    template_name = 'delete_confirm.html'
    pk_url_kwarg = 'workplace_id'

    def get_success_url(self):
        return self.object.department.get_absolute_url()
