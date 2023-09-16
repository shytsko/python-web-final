from django.contrib import admin
from .models import WorkplaceFactor, Workplace

class WorkplaceFactorInline(admin.TabularInline):
    model = WorkplaceFactor
    fields = ('factor', 'condition_class')


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'department',)
    ordering = ('department', 'name',)
    inlines = (WorkplaceFactorInline,)
