from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('patient-data/', views.patient_data_form, name='patient_data_form'),
    path('success/', views.success_view, name='success'),
]
