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
