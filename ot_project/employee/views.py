from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView

from company.mixins import CompanyOwnerTestMixin
from employee.models import Employee
from home.mixins import ContextExMixin
from user.mixins import LoginRequiredMixinEx


class EmployeeDetailView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employee/employee_detail.html'
    pk_url_kwarg = 'employee_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workplaces'] = self.object.employeeworkplace_set.all()
        context['briefings'] = self.object.briefings.all()
        context['knowledge_tests'] = self.object.knowledge_tests.all()
        context['medical_checkups'] = self.object.medical_checkups.all()
        return context


class EmployeeCreateView(LoginRequiredMixinEx, ContextExMixin, CreateView):
    model = Employee
    fields = ('personnel_number', 'last_name', 'first_name', 'middle_name', 'birth_date', 'hiring_date', 'address')
    template_name = 'employee/employee_create.html'

    # def get_success_url(self):
    #     return reverse_lazy('employee_update', kwargs={'employee_id': self.object.pk})

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super(EmployeeCreateView, self).form_valid(form)


class EmployeeDeleteView(LoginRequiredMixinEx, CompanyOwnerTestMixin, ContextExMixin, DeleteView):
    model = Employee
    template_name = 'delete_confirm.html'
    pk_url_kwarg = 'employee_id'
    success_url = reverse_lazy('company')
