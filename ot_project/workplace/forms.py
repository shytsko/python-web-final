from django.forms import ModelForm, CheckboxSelectMultiple

from .models import WorkplaceFactor, Workplace


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