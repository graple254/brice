from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal, InvalidOperation
import uuid
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from django.utils import timezone
from datetime import timedelta

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    url_path = models.CharField(max_length=500, blank=True, null=True)
    method = models.CharField(max_length=10, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    visit_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ip_address or 'Unknown IP'} visited {self.url_path} on {self.visit_date}"



class User(AbstractUser):
    STAFF = "staff"
    DENTIST = "dentist"

    ROLE_CHOICES = [
        (STAFF, "Staff"),
        (DENTIST, "Dentist"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        db_index=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"







# class PasswordReset(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     token = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_used = models.BooleanField(default=False)
#
#     def is_expired(self):
#         # 15 minutes expiry or whatever you want
#         expiry_time = self.created_at + timedelta(minutes=15)
#         return timezone.now() > expiry_time


class Staff(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.full_name



class Dentist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="dentist_profile"
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name




class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()  # Max 60 enforced
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.duration_minutes > 60:
            raise ValidationError("Service duration cannot exceed 60 minutes.")

    def __str__(self):
        return self.name



class DentistService(models.Model):
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("dentist", "service")

    def __str__(self):
        return f"{self.dentist} - {self.service}"
    


class DentistSchedule(models.Model):
    dentist = models.OneToOneField(
        Dentist,
        on_delete=models.CASCADE,
        related_name="schedule"
    )
    work_start = models.TimeField()  # e.g., 09:00
    lunch_start = models.TimeField()  # e.g., 13:00
    lunch_end = models.TimeField()    # e.g., 14:00
    work_end = models.TimeField()     # e.g., 17:00

    def __str__(self):
        return f"Schedule for {self.dentist}"



class TimeBlock(models.Model):
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_reserved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("dentist", "date", "start_time")
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.dentist} | {self.date} {self.start_time}-{self.end_time}"



class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(db_index=True)

    def __str__(self):
        return self.full_name



class Appointment(models.Model):
    BOOKED = "booked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

    STATUS_CHOICES = [
        (BOOKED, "Booked"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
        (NO_SHOW, "No Show"),
    ]

    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=BOOKED
    )
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} with {self.dentist} at {self.start_time}"



class AppointmentBlock(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="blocks")
    block = models.OneToOneField(TimeBlock, on_delete=models.CASCADE)

