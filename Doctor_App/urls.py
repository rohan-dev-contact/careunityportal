from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.doctorDash, name='doctor_dashboard'),
    path('patient_list',views.patient_list,name='patient_list'),
    # path('get_patient_details/<int:patient_id>/', views.get_patient_details, name='get_patient_details'),
]
