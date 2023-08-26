from django.contrib import admin
from .models import Company, Department


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'unp',)
    ordering = ('name',)
    inlines = (DepartmentInline,)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('company', 'name',)
    ordering = ('company', 'name',)
    list_filter = ('company',)
