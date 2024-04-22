from django.urls import path
from Doctor_App import views

urlpatterns = [
    path('dash/', views.doctorDash, name='doctor_dashboard'),
    path('dashboard/', views.patientDash, name='patient_dashboard'),
    path('patient_list/', views.patient_list,name='patient_list'),
    path('patient_list/<patient_id>/', views.patient_detail, name='patient_detail'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('patient/<patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patient/<patient_id>/delete/', views.delete_patient, name='delete_patient'),
    # path('get_patient_details/<int:patient_id>/', views.get_patient_details, name='get_patient_details'),
     path('add_prescription/<str:patient_id>/', views.add_prescription, name='add_prescription'),
    path('add_prescription/<str:patient_id>/<int:follow_up_id>/', views.add_prescription, name='add_follow_up_prescription'),
    path('prescription/<int:prescription_id>/edit/', views.edit_prescription, name='edit_prescription'),
    path('prescription/<int:prescription_id>/', views.view_prescription, name='view_prescription'),
    path('print_prescription/<int:prescription_id>/', views.print_prescription, name='print_prescription'),
    path('patient_prescriptions/', views.patient_prescription_list, name='patient_prescription_list'),
    path('prescription_details/<int:prescription_id>/', views.prescription_details, name='prescription_detail'),
    path('find-doctor/', views.find_doctor, name='find_doctor'),
    path('doctors/<int:doctor_id>/<int:department_id>', views.doctor_details, name='doctor_details'),
    path('book_appointment/<int:department_id>/<int:doctor_id>/', views.book_appointment, name='book_appointment'),

]
