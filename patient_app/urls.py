from django.urls import path
from . import views
from Doctor_App.views import add_patient
from .views import appointment
urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact_view, name='contact'),
    path('signup/', add_patient, name='signup'),
    path('terms/', views.terms, name='terms'),
    path('login/',views.userLogin,name='login'),
    path('logout/',views.userLogout,name='logout'),
    path('appointment/',views.appointment, name='appointment')
]
