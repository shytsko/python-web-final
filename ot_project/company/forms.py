from django.core.exceptions import ValidationError
from django.forms import ModelForm, HiddenInput, TextInput, CheckboxSelectMultiple
from .models import Company, Factor, FactorCondition, FactorGroupChoices, DangerClassChoices, WorkplaceFactor, Workplace


class CompanyHiddenForm(ModelForm):
    class Meta:
        model = Company
        fields = ('unp',)
        widgets = {'unp': HiddenInput()}


class FactorCreateForm(ModelForm):
    class Meta:
        model = Factor
        fields = "__all__"
        widgets = {'company': HiddenInput()}

    def clean_danger_class(self):
        group = self.cleaned_data['group']
        danger_class = self.cleaned_data['danger_class']

        if (group in {FactorGroupChoices.CHEMICAL, FactorGroupChoices.BIOLOGICAL, FactorGroupChoices.DUST} and
                danger_class == DangerClassChoices.NOT_APPLY):
            raise ValidationError("Для фактора должен быть установлен класс опасности")
        return danger_class


class FactorConditionInlineForm(ModelForm):
    class Meta:
        model = FactorCondition
        exclude = ('factor',)
        widgets = {'condition_class': TextInput(attrs={'readonly': 'readonly'})}


class WorkplaceFactorInlineForm(ModelForm):
    company_id = None

    class Meta:
        model = WorkplaceFactor
        exclude = ('workplace',)

    def __init__(self, *args, **kwargs):
        super(WorkplaceFactorInlineForm, self).__init__(*args, **kwargs)
        if self.company_id:
            self.fields['factor'].queryset = self.fields['factor'].queryset.filter(company_id=self.company_id)


class WorkplaceUpdateForm(ModelForm):
    company_id = None

    class Meta:
        model = Workplace
        fields = ('name', 'extra_description', 'code', 'dangerous_works', 'medic_works', 'is_need_internship',
                  'is_need_knowledge_test', 'knowledge_test_period')
        widgets = {
            'dangerous_works': CheckboxSelectMultiple(),
            'medic_works': CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(WorkplaceUpdateForm, self).__init__(*args, **kwargs)

        if self.company_id:
            self.fields['dangerous_works'].queryset = self.fields['dangerous_works'].queryset.filter(
                company_id=self.company_id)
            self.fields['medic_works'].queryset = self.fields['medic_works'].queryset.filter(company_id=self.company_id)
