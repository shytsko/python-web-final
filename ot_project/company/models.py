from django.db import models


class Company(models.Model):
    """
    Данные организации
    name - Название организации
    unp -  УНП
    address - адрес
    tel - телефон
    fax - факс
    email - email
    head - руководитель организации
    """
    name = models.CharField(max_length=100)
    unp = models.CharField(max_length=9)
    address = models.CharField(max_length=100)
    tel = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=15)
    # head = models.ForeignKey("employee.Employee", null=True, default=None, related_name="+", on_delete=models.SET_NULL)


class Department(models.Model):
    """
    Структурные подразделения организации
    company - организация
    name - наименование структурного подразделения
    head - руководитель структурного подразделения
    """
    company = models.ForeignKey("Company", related_name="departments", on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    # head = models.ForeignKey("employee.Employee", null=True, default=None, related_name="+", on_delete=models.SET_NULL)
