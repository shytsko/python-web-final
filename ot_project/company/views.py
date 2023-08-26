from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CompanyForm, DepartmentsFormSet


@login_required
def company_view(request):
    context = {'title': 'Организация'}
    company = request.user.company
    context['company'] = company
    if company:
        if request.method == 'POST':
            form = CompanyForm(request.POST, request.FILES, instance=company)
            formset = DepartmentsFormSet(request.POST, instance=company)
            if formset.is_valid() and form.is_valid():
                form.save()
                formset.save()
        else:
            form = CompanyForm(instance=company)
            formset = DepartmentsFormSet(instance=company)
        context['form'] = form
        context['formset'] = formset
    return render(request, 'company/company.html', context)
