from django.db import models
from django.urls import reverse_lazy

from company.models import Company
from workplace.models import Workplace


class Employee(models.Model):
    company = models.ForeignKey(Company, related_name="employees", on_delete=models.PROTECT, editable=False)
    personnel_number = models.CharField(verbose_name="Табельный номер", max_length=10, unique=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100)
    first_name = models.CharField(verbose_name="Имя", max_length=100)
    middle_name = models.CharField(verbose_name="Отчество", max_length=100, blank=True, null=True)
    birth_date = models.DateField(verbose_name="Дата рождения")
    hiring_date = models.DateField(verbose_name="Дата приема")
    dismissal_date = models.DateField(verbose_name="Дата увольнения", blank=True, null=True)
    address = models.CharField(verbose_name="Домашний адрес", max_length=255, blank=True, null=True)
    workplaces = models.ManyToManyField(Workplace, verbose_name="Рабочие места", through='EmployeeWorkplace',
                                        blank=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def get_absolute_url(self):
        return reverse_lazy("employee_detail", kwargs={"employee_id": self.pk})

    def get_owner_company_id(self):
        return self.company_id

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}" + f" {self.middle_name}" if self.middle_name else ""

    @property
    def short_name(self):
        return f"{self.last_name} {self.first_name[0]}." + f" {self.middle_name[0]}." if self.middle_name else ""

    def __str__(self):
        return self.full_name


class EmployeeWorkplace(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE, verbose_name="Рабочее место")
    date_start = models.DateField(verbose_name="Дата начала работы")
    date_end = models.DateField(verbose_name="Дата окончания работы", blank=True, null=True)

    class Meta:
        ordering = ['date_start', ]
        unique_together = ('employee_id', 'workplace_id')


class Briefing(models.Model):
    class BriefingTypeChoices(models.IntegerChoices):
        INTRODUCTORY = 1, "Вводный"
        PRIMARY = 2, "Первичный"
        REPEATED = 3, "Повторный"
        TARGETED = 4, "Целевой"
        UNSCHEDULED = 5, "Внеплановый"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник", related_name="briefings")
    date = models.DateField(verbose_name="Дата")
    type = models.PositiveSmallIntegerField(verbose_name="Вид", choices=BriefingTypeChoices.choices)

    class Meta:
        ordering = ['employee', 'date']
        verbose_name = "Инструктаж"
        verbose_name_plural = "Инструктажи"


class KnowledgeTest(models.Model):
    class KnowledgeTestTypeChoices(models.IntegerChoices):
        PRIMARY = 1, "Первичная"
        PERIODIC = 2, "Периодическая"
        REPEATED = 3, "Повторная"
        UNSCHEDULED = 4, "Внеплановая"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник",
                                 related_name="knowledge_tests")
    type = models.PositiveSmallIntegerField(verbose_name="Вид", choices=KnowledgeTestTypeChoices.choices)
    date = models.DateField(verbose_name="Дата")
    protocol_number = models.PositiveIntegerField(verbose_name="Номер протокола")

    class Meta:
        ordering = ['employee', 'date']
        verbose_name = "Проверка знаний"
        verbose_name_plural = "Проверки знаний"


class MedicalCheck(models.Model):
    class MedicalCheckTypeChoices(models.IntegerChoices):
        PRELIMINARY = 1, "Предварительный"
        PERIODIC = 2, "Периодический"
        UNSCHEDULED = 3, "Внеплановый"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник",
                                 related_name="medical_checkups")
    type = models.PositiveSmallIntegerField(verbose_name="Вид", choices=MedicalCheckTypeChoices.choices)
    date = models.DateField(verbose_name="Дата")

    class Meta:
        ordering = ['employee', 'date']
        verbose_name = "Медицинский осмотр"
        verbose_name_plural = "Медицинские осмотр"
