from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy


class FactorGroupChoices(models.IntegerChoices):
    CHEMICAL = 1, "Химические"
    BIOLOGICAL = 2, "Биологические"
    DUST = 3, "Пыли и аэрозоли"
    PHYSICAL = 4, "Физические"
    HEAVY = 5, "Тяжесть"
    STRESSFUL = 6, "Напряженность"


class DangerClassChoices(models.IntegerChoices):
    NOT_APPLY = 0, "Не применяется"
    CLASS_1 = 1, "1"
    CLASS_2 = 2, "2"
    CLASS_3 = 3, "3"
    CLASS_4 = 4, "4"


class MedicPeriodChoices(models.IntegerChoices):
    YEAR_1 = 1, "1 год"
    YEAR_2 = 2, "2 года"
    YEAR_3 = 3, "3 года"
    __empty__ = "Не требуется"


class ConditionClassChoices(models.TextChoices):
    CONDITION_2 = "2", "2"
    CONDITION_3_1 = "3.1", "3.1"
    CONDITION_3_2 = "3.2", "3.2"
    CONDITION_3_3 = "3.3", "3.3"
    CONDITION_3_4 = "3.4", "3.4"
    CONDITION_4 = "4", "4"


class Company(models.Model):
    """
    Данные организации
    name - Название организации
    unp - 9-значный учетный номер плательщика, должен быть уникальным
    address - адрес
    tel - номер телефона
    fax - номер факса
    email - email, должен быть уникальным
    head - руководитель организации
    """
    name = models.CharField(verbose_name="Название", max_length=100)
    unp = models.CharField(verbose_name="УНП", max_length=9, unique=True,
                           validators=[
                               RegexValidator(regex=r'^\d{9}$', message="УНП должен состоять из 9 цифр")
                           ])
    address = models.CharField(verbose_name="Адрес", max_length=100)
    tel = models.CharField(verbose_name="Номер телефона", max_length=20, null=True, blank=True)
    fax = models.CharField(verbose_name="Номер факс", max_length=20, null=True, blank=True)
    email = models.EmailField(verbose_name="E-mail", max_length=100, unique=True, )

    # head = models.ForeignKey("employee.Employee", null=True, default=None, related_name="+", on_delete=models.SET_NULL)

    class Meta:
        ordering = ["name"]
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return f"({self.unp}) {self.name}"


class Department(models.Model):
    """
    Структурные подразделения организации
    company - организация
    name - наименование структурного подразделения
    head - руководитель структурного подразделения
    """
    company = models.ForeignKey("Company", related_name="departments", on_delete=models.PROTECT, editable=False)
    name = models.CharField(verbose_name="Название", max_length=100)

    # head = models.ForeignKey("employee.Employee", null=True, default=None, related_name="+", on_delete=models.SET_NULL)

    class Meta:
        ordering = ["name"]
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        unique_together = ('company', 'name')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse_lazy("department_detail", kwargs={"department_id": self.pk})

    def get_owner_company_id(self):
        return self.company_id


class DangerousWork(models.Model):
    company = models.ForeignKey("Company", related_name="dangerous_works", on_delete=models.PROTECT, editable=False)
    name = models.CharField(verbose_name="Название", max_length=250)

    class Meta:
        ordering = ["name"]
        verbose_name = "Опасная работа"
        verbose_name_plural = "Опасные работы"
        unique_together = ('company', 'name')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse_lazy("dangerous_work_detail", kwargs={"dangerous_work_id": self.pk})

    def get_owner_company_id(self):
        return self.company_id


class MedicWork(models.Model):
    company = models.ForeignKey("Company", related_name="medic_works", on_delete=models.PROTECT, editable=False)
    name = models.CharField(verbose_name="Название", max_length=250)
    punct = models.CharField(verbose_name="Пункт приложения", max_length=10)
    medical_period = models.SmallIntegerField(verbose_name="Периодичность медосмотров",
                                              choices=MedicPeriodChoices.choices)

    class Meta:
        ordering = ["name"]
        verbose_name = "Работа, требующая медосмотра"
        verbose_name_plural = "Работы, требующие медосмотров"
        unique_together = ('company', 'name')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse_lazy("medic_work_detail", kwargs={"medic_work_id": self.pk})

    def get_owner_company_id(self):
        return self.company_id


class Factor(models.Model):
    company = models.ForeignKey("Company", related_name="factors", on_delete=models.PROTECT, editable=False)
    group = models.PositiveSmallIntegerField(verbose_name="Группа", choices=FactorGroupChoices.choices)
    name = models.CharField(verbose_name="Название", max_length=250, unique=True)
    punct = models.CharField(verbose_name="Пункт приложения", max_length=10)
    danger_class = models.PositiveSmallIntegerField(verbose_name="Класс опасности", choices=DangerClassChoices.choices,
                                                    default=DangerClassChoices.NOT_APPLY)
    is_allergen = models.BooleanField(verbose_name="Аллерген", default=False)
    is_carcinogen = models.BooleanField(verbose_name="Канцероген", default=False)

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        if self.group in {FactorGroupChoices.CHEMICAL, FactorGroupChoices.BIOLOGICAL, FactorGroupChoices.DUST}:
            if self.danger_class == DangerClassChoices.NOT_APPLY:
                raise ValidationError("Для фактора должен быть установлен класс опасности")
        else:
            self.danger_class = DangerClassChoices.NOT_APPLY
            self.is_allergen = False
            self.is_carcinogen = False

    def save(self, *args, **kwargs):
        pre_save_pk = self.pk
        super().save(*args, **kwargs)
        if not pre_save_pk:
            for condition_class in ConditionClassChoices.values:
                FactorCondition.objects.create(factor=self, condition_class=condition_class)

    class Meta:
        ordering = ["name"]
        verbose_name = "Вредный или опасный производственный фактор"
        verbose_name_plural = "Вредные и опасные производственные факторы"
        unique_together = ('company', 'name')

    def get_absolute_url(self):
        return reverse_lazy("factor_detail", kwargs={"factor_id": self.pk})

    def get_owner_company_id(self):
        return self.company_id


class FactorCondition(models.Model):
    factor = models.ForeignKey("Factor", verbose_name="Фактор", editable=False, related_name="conditions",
                               on_delete=models.CASCADE)
    condition_class = models.CharField(max_length=3, verbose_name="Класс условий труда",
                                       choices=ConditionClassChoices.choices)
    is_need_prev_medical = models.BooleanField(default=False, verbose_name="Необходим предварительный медосмотр")
    medical_period = models.SmallIntegerField(verbose_name="Периодичность медосмотров",
                                              choices=MedicPeriodChoices.choices, blank=True, null=True)

    class Meta:
        ordering = ['factor', 'condition_class']
        verbose_name = "Класс условий труда"
        verbose_name_plural = "Классы условий труда"
        unique_together = ('factor', 'condition_class')


class Workplace(models.Model):
    department = models.ForeignKey("Department", related_name="workplaces", on_delete=models.PROTECT, editable=False)
    name = models.CharField(verbose_name="Название", max_length=100)
    extra_description = models.CharField(verbose_name="Дополнительное описание", max_length=100, null=True, blank=True)
    code = models.CharField(verbose_name="Код должности/профессии", max_length=8,
                            validators=[RegexValidator(regex=r'^\d{4}-\d{3}$',
                                                       message="Код должен соответствовать шаблону XXXX-XXX (X - число)")
                                        ])
    is_office_worker = models.BooleanField(default=False, verbose_name="Должность служащего", editable=False)
    factors = models.ManyToManyField('Factor', through='WorkplaceFactor',
                                     verbose_name="Вредные и опасные производственные факторы")
    dangerous_works = models.ManyToManyField(DangerousWork, verbose_name="Работы с повышенной опасностью", blank=True)
    medic_works = models.ManyToManyField(MedicWork, verbose_name="Работы, требующие медосмотров", blank=True)
    is_need_internship = models.BooleanField(default=False, verbose_name="Требуется стажировка")
    is_need_knowledge_test = models.BooleanField(default=False, verbose_name="Требуется проверка знаний")
    knowledge_test_period = models.SmallIntegerField(verbose_name="Периодичность проверки знаний в месяцах",
                                                     blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy('workplace_detail', kwargs={'workplace_id': self.pk})

    def get_owner_company_id(self):
        return self.department.company_id

    def clean(self):
        self.is_office_worker = self.code[0] in '123'

        if self.pk is not None:
            if not self.is_office_worker:
                if self.dangerous_works.count() > 0:
                    self.is_need_internship = True
                    self.is_need_knowledge_test = True
                else:
                    self.is_need_internship = False
                    self.is_need_knowledge_test = False

            if self.is_need_knowledge_test:
                if not self.knowledge_test_period:
                    self.knowledge_test_period = 36 if self.is_office_worker else 12
            else:
                self.knowledge_test_period = None

    def __str__(self):
        return f"{self.department.name} - {self.name}"

    class Meta:
        ordering = ['department', 'name']
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        unique_together = ('department', 'name')


class WorkplaceFactor(models.Model):
    workplace = models.ForeignKey('Workplace', on_delete=models.CASCADE)
    factor = models.ForeignKey('Factor', on_delete=models.CASCADE, verbose_name="Фактор", )
    condition_class = models.CharField(max_length=3, verbose_name="Класс условий труда",
                                       choices=ConditionClassChoices.choices)

    class Meta:
        ordering = ['factor__name', ]
        unique_together = ('workplace_id', 'factor_id')
