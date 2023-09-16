from django.core.exceptions import ValidationError
from django.forms import ModelForm, HiddenInput, TextInput
from .models import Company, Factor, FactorCondition, FactorGroupChoices, DangerClassChoices


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
