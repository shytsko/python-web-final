from django.db import models

from workplace.models import Workplace


class Employee(models.Model):
    personnel_number = models.CharField(verbose_name="Табельный номер", max_length=10, unique=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100)
    first_name = models.CharField(verbose_name="Имя", max_length=100)
    middle_name = models.CharField(verbose_name="Отчество", max_length=100, blank=True, null=True)
    birth_date = models.DateField(verbose_name="Дата рождения")
    address = models.CharField(verbose_name="Домашний адрес", max_length=255, blank=True, null=True)
    workplaces = models.ManyToManyField(Workplace, verbose_name="Рабочие места", through='EmployeeWorkplace',
                                        blank=True)

    class Meta:
        ordering = ['department', 'name']
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


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
        CHEMICAL = 1, "Вводный"
        BIOLOGICAL = 2, "Первичный"
        DUST = 3, "Повторный"
        PHYSICAL = 4, "Целевой"
        HEAVY = 5, "Внеплановый"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник", related_name="briefings")
    date = models.DateField(verbose_name="Дата")
    type = models.PositiveSmallIntegerField(verbose_name="Группа", choices=BriefingTypeChoices.choices)
