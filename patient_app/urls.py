from django.urls import path
from patient_app import views
from Doctor_App.views import add_patient
urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact_view, name='contact'),
    path('signup/', add_patient, name='signup'),
    path('terms/', views.terms, name='terms'),
    path('login/',views.userLogin,name='login'),
    path('logout/',views.userLogout,name='logout'),
    path('appointment/',views.appointment, name='appointment'),
    path('upload_file/',views.upload_file, name='upload_file'), 
    path('reset-password/', views.passwordResetRequestView, name='password_reset_request'),
    path('verify-otp/<str:username>/', views.verify_otp, name='verify_otp'),
    path('reset_password/<str:username>/', views.reset_password, name='reset_password'),
]