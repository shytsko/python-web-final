from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
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
    name = models.CharField(verbose_name="Название", max_length=100, )

    # head = models.ForeignKey("employee.Employee", null=True, default=None, related_name="+", on_delete=models.SET_NULL)

    class Meta:
        ordering = ["name"]
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        unique_together = ('company', 'name')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse_lazy("department_detail", kwargs={"depatrment_id": self.pk})

    def get_owner_company(self):
        return self.company


class DangerousWork(models.Model):
    company = models.ForeignKey("Company", related_name="dangerous_works", on_delete=models.PROTECT)
    name = models.CharField(verbose_name="Название", max_length=250, unique=True)

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
    name = models.CharField(verbose_name="Название", max_length=250, unique=True)
    punct = models.CharField(verbose_name="Пункт приложения", max_length=10)

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


class FactorGroup(models.Model):
    group = models.CharField(verbose_name="Группа", max_length=15, unique=True)

    def __str__(self):
        return f"{self.group}"

    class Meta:
        verbose_name = "Группа вредных и опасных производственных факторов"
        verbose_name_plural = "Группа вредных и опасных производственных факторов"


CONDITION_CLASS_CHOICES = (
    ("2", "2 - Допустимые"),
    ("3.1", "3.1 - Вредные первой степени"),
    ("3.2", "3.2 - Вредные второй степени"),
    ("3.3", "3.3 - Вредные третьей степени"),
    ("3.4", "3.4 - Вредные четвертой степени"),
    ("4", "4 - Опасные"),
)

PERIOD_CHOICES = (
    (0, "Не требуется"),
    (1, "1 год"),
    (2, "2 года"),
    (3, "3 года"),
)


class Factor(models.Model):
    company = models.ForeignKey("Company", related_name="factors", on_delete=models.PROTECT)
    group = models.ForeignKey("FactorGroup", verbose_name="Группа", related_name="factors",
                              on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name="Название", max_length=250, unique=True)
    punct = models.CharField(verbose_name="Пункт приложения", max_length=10)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        pre_save_pk = self.pk
        super().save(*args, **kwargs)
        if not pre_save_pk:
            for condition_class, _ in CONDITION_CLASS_CHOICES:
                FactorCondition.objects.create(factor=self, condition_class=condition_class)

    class Meta:
        ordering = ["name"]
        verbose_name = "Вредный или опасный производственный фактор"
        verbose_name_plural = "Вредные и опасные производственные факторы"

    # def get_absolute_url(self):
    #     return reverse_lazy("factor_detail", kwargs={"factor_id": self.pk})

    def get_owner_company(self):
        return self.company


class FactorCondition(models.Model):
    factor = models.ForeignKey("Factor", verbose_name="Фактор", related_name="conditions", on_delete=models.CASCADE)
    condition_class = models.CharField(max_length=250, verbose_name="Класс условий", choices=CONDITION_CLASS_CHOICES)
    is_need_prev_medical = models.BooleanField(default=False, verbose_name="Необходим предварительный медосмотр")
    medical_period = models.PositiveSmallIntegerField(verbose_name="Периодичность медосмотров",
                                                      default=0, choices=PERIOD_CHOICES)

    class Meta:
        ordering = ["factor"]
        verbose_name = "Класс условий труда"
        verbose_name_plural = "Классы условий труда"
        unique_together = ('factor', 'condition_class')
