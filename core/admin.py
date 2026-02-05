from django.contrib import admin
from . models import *

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'session_key', 'url_path', 'method', 'visit_date', 'location')
    list_filter = ('method', 'visit_date', 'location')
    search_fields = ('ip_address', 'session_key', 'url_path', 'referrer', 'user_agent')
    readonly_fields = ('visit_date',)
    ordering = ('-visit_date',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "email", "phone")
    search_fields = ("full_name", "email", "phone")



@admin.register(Dentist)
class DentistAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "email", "phone", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "email", "phone")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_minutes", "is_active", "created_by")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(DentistService)
class DentistServiceAdmin(admin.ModelAdmin):
    list_display = ("dentist", "service", "assigned_by", "assigned_at")
    list_filter = ("dentist", "service")
    search_fields = ("dentist__full_name", "service__name")



@admin.register(DentistSchedule)
class DentistScheduleAdmin(admin.ModelAdmin):
    list_display = ("dentist", "work_start", "lunch_start", "lunch_end", "work_end")
    search_fields = ("dentist__full_name",)



@admin.register(TimeBlock)
class TimeBlockAdmin(admin.ModelAdmin):
    list_display = ("dentist", "date", "start_time", "end_time", "is_reserved")
    list_filter = ("dentist", "date", "is_reserved")
    search_fields = ("dentist__full_name",)



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone")
    search_fields = ("full_name", "email", "phone")



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "dentist", "service", "start_time", "end_time", "status", "created_by")
    list_filter = ("status", "dentist", "service")
    search_fields = ("patient__full_name", "dentist__full_name", "service__name")
    date_hierarchy = "start_time"



@admin.register(AppointmentBlock)
class AppointmentBlockAdmin(admin.ModelAdmin):
    list_display = ("appointment", "block")
    search_fields = ("appointment__patient__full_name", "appointment__dentist__full_name")
