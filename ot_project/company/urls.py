from django.urls import path
from .views import company_view

urlpatterns = [
    path('', company_view, name='company')
]
