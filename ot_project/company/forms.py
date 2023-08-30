from django.forms import ModelForm, HiddenInput
from .models import Company


class CompanyHiddenForm(ModelForm):
    class Meta:
        model = Company
        fields = ('unp',)
        widgets = {'unp': HiddenInput()}
