from django.urls import path
from .views import WorkplaceCreateView, WorkplaceDetailView, WorkplaceUpdateView, WorkplaceDeleteView

urlpatterns = [
    path('create/department/<int:department_id>', WorkplaceCreateView.as_view(), name='workplace_create'),
    path('<int:workplace_id>/', WorkplaceDetailView.as_view(), name='workplace_detail'),
    path('<int:workplace_id>/update', WorkplaceUpdateView.as_view(), name='workplace_update'),
    path('<int:workplace_id>/delete', WorkplaceDeleteView.as_view(), name='workplace_delete'),
]
