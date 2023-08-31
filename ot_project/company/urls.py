from django.urls import path
from .views import CompanyDetailView, CompanyUpdateView, DepartmentDetailView, CompanyDepartmentsSetUpdateView, \
    CompanyDangerousWorksSetUpdateView, DangerousWorkDetailView, MedicWorkDetailView, CompanyMedicWorksSetUpdateView, \
    FactorDetailView

urlpatterns = [
    path('', CompanyDetailView.as_view(), name='company'),
    path('update/', CompanyUpdateView.as_view(), name='company_update'),
    path('department/<int:depatrment_id>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('departments/update/', CompanyDepartmentsSetUpdateView.as_view(), name='departments_update'),
    path('dangerous-work/<int:dangerous_work_id>/', DangerousWorkDetailView.as_view(), name='dangerous_work_detail'),
    path('dangerous-works/update/', CompanyDangerousWorksSetUpdateView.as_view(), name='dangerous_works_update'),
    path('medic-work/<int:medic_work_id>/', MedicWorkDetailView.as_view(), name='medic_work_detail'),
    path('medic-works/update/', CompanyMedicWorksSetUpdateView.as_view(), name='medic_works_update'),
    path('factor/<int:factor_id>/', FactorDetailView.as_view(), name='factor_detail'),
]
