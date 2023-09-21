from django.urls import path
from .views import EmployeeCreateView, EmployeeDetailView, EmployeeDeleteView

urlpatterns = [
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:employee_id>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:employee_id>/update', EmployeeDetailView.as_view(), name='employee_update'),
    path('<int:employee_id>/delete', EmployeeDeleteView.as_view(), name='employee_delete'),
]
