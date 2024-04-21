from django.contrib import admin
from django.contrib.auth.models import Group

from patient_app.forms import PlainTextPasswordUserCreationForm
from patient_app.models import Specialization, User,Department,Doctor,Patient
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.site_header='CareUnity Portal'
admin.site.site_title='Administration'
admin.site.index_title='CareUnity Portal'
admin.site.unregister(Group)

# admin.site.register(Contact)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display=('username','first_name','last_name','email','is_staff','is_active','address','mobile','is_superuser','last_login','id')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=('username','name','email','health_condition','assigned_doctor','health_insurance','age')
    list_filter = ('health_condition','assigned_doctor','health_insurance','age')
    search_fields = ('user__username', 'health_condition','assigned_doctor','health_insurance')
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'
    
    def name(self, obj):
        return obj.user.first_name+' '+obj.user.last_name
    email.short_description = 'Name'



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display=('username','email','get_specializations','get_departments','experience',)
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

    def get_departments(self, obj):
        return ', '.join([s.department_name for s in obj.departments.all()])
    get_departments.short_description = 'Departments'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display=('department_name', 'id', 'head_of_department', 'location', 'contact_phone', 'contact_email', 'emergency_services')
    list_filter = ('emergency_services',)
    search_fields = ('department_name', 'location', 'contact_phone', 'contact_email')
    fieldsets = (
        (None, {
            'fields': ('department_name', 'work_description', 'intended_patients', 'treated_diseases')
        }),
        ('Department Details', {
            'fields': ('head_of_department', 'location', 'contact_phone', 'contact_email', 'special_facilities', 'operating_hours', 'emergency_services', 'insurance_accepted'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display=('name','id')
    search_fields = ('name',)


class CustomUserAdmin(UserAdmin):
    add_form = PlainTextPasswordUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'address', 'mobile')}
        ),
    )

admin.site.register(User, CustomUserAdmin)