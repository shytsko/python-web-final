from django.urls import path
from .views import CompanyDetailView, CompanyUpdateView, DepartmentDetailView, CompanyDepartmentsSetUpdateView

urlpatterns = [
    path('', CompanyDetailView.as_view(), name='company'),
    path('update/', CompanyUpdateView.as_view(), name='company_update'),
    path('department/<int:depatrment_id>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('departments/update/', CompanyDepartmentsSetUpdateView.as_view(), name='departments_update'),
]
