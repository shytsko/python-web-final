from django.contrib import admin
from .models import Company, Department


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'unp',)
    ordering = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('company', 'name',)
    ordering = ('company', 'name',)
    list_filter = ('company',)
