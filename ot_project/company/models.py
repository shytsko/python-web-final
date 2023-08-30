from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy


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
    company = models.ForeignKey("Company", related_name="departments", on_delete=models.PROTECT)
    name = models.CharField(verbose_name="Название", max_length=100)

    # head = models.ForeignKey("employee.Employee", null=True, default=None, related_name="+", on_delete=models.SET_NULL)

    class Meta:
        ordering = ["name"]
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse_lazy("department_detail", kwargs={"depatrment_id": self.pk})

    def get_owner_company(self):
        return self.company


class DangerousWork(models.Model):
    company = models.ForeignKey("Company", related_name="dangerous_works", on_delete=models.PROTECT)
    name = models.CharField(verbose_name="Название", max_length=250)

    class Meta:
        ordering = ["name"]
        verbose_name = "Опасная работа"
        verbose_name_plural = "Опасные работы"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse_lazy("dangerous_work_detail", kwargs={"dangerous_work_id": self.pk})

    def get_owner_company(self):
        return self.company


class MedicWork(models.Model):
    company = models.ForeignKey("Company", related_name="medic_works", on_delete=models.PROTECT)
    name = models.CharField(verbose_name="Название", max_length=250)
    punct = models.CharField(verbose_name="Пункт приложени", max_length=10)

    class Meta:
        ordering = ["name"]
        verbose_name = "Работа, требующая медосмотра"
        verbose_name_plural = "Работы, требующие медосмотров"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse_lazy("medic_work_detail", kwargs={"medic_work_id": self.pk})

    def get_owner_company(self):
        return self.company


