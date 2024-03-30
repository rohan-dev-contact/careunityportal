from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.doctorDash, name='doctor_dashboard'),
    path('patient_list',views.patientList,name='patient_list')
]
