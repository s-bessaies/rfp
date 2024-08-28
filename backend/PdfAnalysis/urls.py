from django.urls import path
from . import views

urlpatterns = [
    path('api/extract_attributes/', views.process_pdf, name='process-pdf'),
    path('api/rfp-history/', views.rfp_history, name='rfp-history'),
    path('api/rfp-history-top/', views.rfp_history_top, name='rfp-history'),
]