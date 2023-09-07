from django.contrib import admin
from .models import Company, Department, DangerousWork, MedicWork, Factor, FactorCondition, WorkplaceFactor, Workplace


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


class FactorConditionInline(admin.TabularInline):
    model = FactorCondition
    extra = 0
    can_delete = False
    max_num = 0
    fields = ('condition_class', 'is_need_prev_medical', 'medical_period')
    readonly_fields = ('condition_class',)


@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'company',)
    ordering = ('company', 'name',)
    list_filter = ('company',)
    inlines = (FactorConditionInline,)


class WorkplaceFactorInline(admin.TabularInline):
    model = WorkplaceFactor
    fields = ('factor', 'condition_class')


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'department',)
    ordering = ('department', 'name',)
    inlines = (WorkplaceFactorInline,)