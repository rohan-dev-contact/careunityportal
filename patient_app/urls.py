from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact_view, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('terms/', views.terms, name='terms'),
    path('login/',views.userLogin,name='login'),
    path('logout/',views.userLogout,name='logout')
]
