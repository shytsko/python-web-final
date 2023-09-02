from django.core.exceptions import ValidationError
from django.forms import ModelForm, HiddenInput, TextInput
from .models import Company, Factor, FactorCondition


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

        if (group in {Factor.GroupChoices.CHEMICAL, Factor.GroupChoices.BIOLOGICAL, Factor.GroupChoices.DUST} and
                danger_class == Factor.DangerClassChoices.NOT_APPLY):
            raise ValidationError("Для фактора должен быть установлен класс опасности")
        return danger_class


class FactorConditionInlineForm(ModelForm):
    class Meta:
        model = FactorCondition
        exclude = ('factor',),
        widgets = {'condition_class': TextInput(attrs={'readonly': 'readonly'})}
