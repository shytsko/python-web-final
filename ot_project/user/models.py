from django.contrib.auth.models import AbstractUser
from django.db import models
from company.models import Company


class User(AbstractUser):
    company = models.ForeignKey(Company, null=True, default=None, related_name="+", on_delete=models.PROTECT)
