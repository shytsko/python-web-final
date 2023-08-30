from django.contrib import admin
from .models import Company, Department, DangerousWork, MedicWork, Factor, FactorGroup, FactorCondition


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


class DangerousWorkInline(admin.TabularInline):
    model = DangerousWork
    extra = 1


class MedicWorkInline(admin.TabularInline):
    model = MedicWork
    extra = 1


class FactorInline(admin.TabularInline):
    model = Factor
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'unp',)
    ordering = ('name',)
    inlines = (DepartmentInline, DangerousWorkInline, FactorInline)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company',)
    ordering = ('company', 'name',)
    list_filter = ('company',)


@admin.register(DangerousWork)
class DangerousWorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'company',)
    ordering = ('company', 'name',)
    list_filter = ('company',)


@admin.register(MedicWork)
class DangerousWorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'company',)
    ordering = ('company', 'name',)
    list_filter = ('company',)


@admin.register(FactorGroup)
class FactorGroupAdmin(admin.ModelAdmin):
    list_display = ('group',)
    ordering = ('group',)


class FactorConditionInline(admin.TabularInline):
    model = FactorCondition
    extra = 0
    can_delete = False
    max_num = 0


@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'company',)
    ordering = ('company', 'name',)
    list_filter = ('company',)
    inlines = (FactorConditionInline,)
