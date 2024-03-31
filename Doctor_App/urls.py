from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.doctorDash, name='doctor_dashboard'),
    path('dashboard/', views.patientDash, name='patient_dashboard'),
    path('patient_list/',views.patient_list,name='patient_list'),
    path('patient_list/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('patient/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patient/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
    # path('get_patient_details/<int:patient_id>/', views.get_patient_details, name='get_patient_details'),
]
