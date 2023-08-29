from django.urls import path
from .views import CompanyDetailView, CompanyUpdateView, DepartmentDetailView

urlpatterns = [
    path('', CompanyDetailView.as_view(), name='company'),
    path('update/', CompanyUpdateView.as_view(), name='company_update'),
    path('update/department/<int:depatrment_id>', DepartmentDetailView.as_view(), name='department_detail'),
]
