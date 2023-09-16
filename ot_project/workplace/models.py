from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Min
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse_lazy
from company.models import DangerousWork, MedicWork, MedicPeriodChoices, ConditionClassChoices, Department, Factor


class Workplace(models.Model):
    department = models.ForeignKey(Department, related_name="workplaces", on_delete=models.PROTECT, editable=False)
    name = models.CharField(verbose_name="Название", max_length=100)
    extra_description = models.CharField(verbose_name="Дополнительное описание", max_length=250, null=True, blank=True)
    code = models.CharField(verbose_name="Код должности/профессии", max_length=8,
                            validators=[RegexValidator(regex=r'^\d{4}-\d{3}$',
                                                       message="Код должен соответствовать шаблону XXXX-XXX (X - число)")
                                        ])
    is_office_worker = models.BooleanField(default=False, verbose_name="Должность служащего", editable=False)
    factors = models.ManyToManyField(Factor, through='WorkplaceFactor',
                                     verbose_name="Вредные и опасные производственные факторы")
    dangerous_works = models.ManyToManyField(DangerousWork, verbose_name="Работы с повышенной опасностью", blank=True)
    medic_works = models.ManyToManyField(MedicWork, verbose_name="Работы, требующие медосмотров", blank=True)
    is_need_internship = models.BooleanField(default=False, verbose_name="Требуется стажировка")
    is_need_knowledge_test = models.BooleanField(default=False, verbose_name="Требуется проверка знаний")
    knowledge_test_period = models.SmallIntegerField(verbose_name="Периодичность проверки знаний в месяцах",
                                                     blank=True, null=True)

    @property
    def is_need_prev_medical_check(self) -> bool:
        return self.medic_works.count() > 0 or self.workplacefactor_set. \
            filter(factor__conditions__condition_class=F("condition_class"),
                   factor__conditions__is_need_prev_medical=True). \
            values_list("factor__conditions__is_need_prev_medical", flat=True).first() is not None

    @property
    def get_period_medical_check(self) -> MedicPeriodChoices | None:
        period = self.workplacefactor_set.filter(factor__conditions__condition_class=F("condition_class")). \
            values_list("factor__conditions__medical_period", flat=True). \
            aggregate(Min("factor__conditions__medical_period"))["factor__conditions__medical_period__min"]
        return MedicPeriodChoices(period) if period is not None else None

    def get_absolute_url(self):
        return reverse_lazy('workplace_detail', kwargs={'workplace_id': self.pk})

    def get_owner_company_id(self):
        return self.department.company_id

    def clean(self):
        self.is_office_worker = self.code[0] in '123'
        self.check_knowledge_test()

    def check_knowledge_test(self):
        if self.pk is not None:
            if self.dangerous_works.count() > 0:
                self.is_need_internship = True
                self.is_need_knowledge_test = True
            else:
                if not self.is_office_worker:
                    self.is_need_internship = False
                    self.is_need_knowledge_test = False

            if self.is_need_knowledge_test:
                if not self.knowledge_test_period:
                    self.knowledge_test_period = 36 if self.is_office_worker else 12
            else:
                self.knowledge_test_period = None

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['department', 'name']
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        unique_together = ('department', 'name')


@receiver(m2m_changed, sender=Workplace.dangerous_works.through)
def cart_update_total_when_item_added(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        instance.check_knowledge_test()
        instance.save()


class WorkplaceFactor(models.Model):
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, verbose_name="Фактор", )
    condition_class = models.CharField(max_length=3, verbose_name="Класс условий труда",
                                       choices=ConditionClassChoices.choices)

    class Meta:
        ordering = ['factor__name', ]
        unique_together = ('workplace_id', 'factor_id')

