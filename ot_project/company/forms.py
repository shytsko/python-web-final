from django.forms import ModelForm, inlineformset_factory
from .models import Company, Department


# class CompanyForm(ModelForm):
#     class Meta:
#         model = Company
#         fields = '__all__'


DepartmentsFormSet = inlineformset_factory(Company, Department, fields=('name',))
