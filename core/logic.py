from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from core.models import *


BLOCK_MINUTES = 15
BOOKING_WINDOW_DAYS = 30



def validate_booking_date(date):
    today = timezone.localdate()
    last_allowed = today + timedelta(days=BOOKING_WINDOW_DAYS)

    if date < today:
        raise ValueError("Cannot book appointments in the past.")

    if date > last_allowed:
        raise ValueError("Date is outside the booking window.")


def get_service_dentists(service):
    return DentistService.objects.filter(
        service=service,
        dentist__is_active=True
    ).values_list("dentist_id", flat=True)



def get_available_slots(service, date):
    validate_booking_date(date)

    required_blocks = service.duration_minutes // BLOCK_MINUTES

    dentist_ids = get_service_dentists(service)

    blocks = (
        TimeBlock.objects
        .filter(
            date=date,
            dentist_id__in=dentist_ids,
            is_reserved=False
        )
        .select_for_update(skip_locked=True)
        .order_by("dentist_id", "start_time")
    )

    slots = []
    buffer = []

    for block in blocks:
        if not buffer:
            buffer = [block]
        else:
            last = buffer[-1]
            if (
                block.dentist_id == last.dentist_id and
                block.start_time == last.end_time
            ):
                buffer.append(block)
            else:
                buffer = [block]

        if len(buffer) == required_blocks:
            slots.append({
                "dentist_id": buffer[0].dentist_id,
                "start_time": buffer[0].start_time,
                "end_time": buffer[-1].end_time,
                "blocks": buffer.copy()
            })
            buffer.pop(0)

    return slots


