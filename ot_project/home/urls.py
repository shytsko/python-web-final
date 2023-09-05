from django.urls import path
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='company'), name='home'),
]
