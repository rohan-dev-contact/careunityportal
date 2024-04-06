from django.urls import path
from .views import add_prescription,add_patient,doctorDash,patient_detail,patient_list,patientDash,edit_patient,delete_patient,edit_prescription,view_prescription,print_prescription

urlpatterns = [
    path('dash/', doctorDash, name='doctor_dashboard'),
    path('dashboard/', patientDash, name='patient_dashboard'),
    path('patient_list/',patient_list,name='patient_list'),
    path('patient_list/<patient_id>/', patient_detail, name='patient_detail'),
    path('add_patient/', add_patient, name='add_patient'),
    path('patient/<patient_id>/edit/', edit_patient, name='edit_patient'),
    path('patient/<patient_id>/delete/', delete_patient, name='delete_patient'),
    # path('get_patient_details/<int:patient_id>/', get_patient_details, name='get_patient_details'),
     path('add_prescription/<str:patient_id>/', add_prescription, name='add_prescription'),
    path('add_prescription/<str:patient_id>/<int:follow_up_id>/', add_prescription, name='add_follow_up_prescription'),
    path('prescription/<int:prescription_id>/edit/', edit_prescription, name='edit_prescription'),
    path('prescription/<int:prescription_id>/', view_prescription, name='view_prescription'),
    path('print_prescription/<int:prescription_id>/', print_prescription, name='print_prescription'),

]
