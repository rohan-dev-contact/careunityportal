from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Specialization, User,Department,Doctor,Patient

# Register your models here.
admin.site.site_header='CareUnity Portal'
admin.site.site_title='Administration'
admin.site.index_title='CareUnity Portal'
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('username','first_name','last_name','email','is_staff','is_active','address','mobile','is_superuser','last_login','id')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=('username','email','health_condition','assigned_doctor','health_insurance','age')
    list_filter = ('health_condition','assigned_doctor','health_insurance','age')
    search_fields = ('user__username', 'health_condition','assigned_doctor','health_insurance')
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display=('username','email','get_specializations','experience',)
    list_filter = ('departments','specialization__name')
    search_fields = ('user__username', 'specialization__name', 'departments__department_name')

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

    def get_specializations(self, obj):
        return ', '.join([s.name for s in obj.specialization.all()])
    get_specializations.short_description = 'Specializations'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display=('department_name','id')
    search_fields = ('department_name',)

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display=('name','id')
    search_fields = ('name',)