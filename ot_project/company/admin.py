from django.contrib import admin
from .models import Company, Department, DangerousWork


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


class DangerousWorkInline(admin.TabularInline):
    model = DangerousWork
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'unp',)
    ordering = ('name',)
    inlines = (DepartmentInline, DangerousWorkInline,)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('company', 'name',)
    ordering = ('company', 'name',)
    list_filter = ('company',)


@admin.register(DangerousWork)
class DangerousWorkAdmin(admin.ModelAdmin):
    list_display = ('company', 'name',)
    ordering = ('company', 'name',)
    list_filter = ('company',)
