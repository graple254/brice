from datetime import datetime, timedelta, time
from django.utils import timezone
from .models import *

def generate_time_blocks_for_dentist(dentist: Dentist, date: datetime.date, break_minutes: int = 15):
    """
    Generates 15-minute time blocks for a dentist on a given date based on their schedule.
    Lunch break is skipped automatically.
    Optional break_minutes are left free between work sessions (after each appointment block generation).
    
    Args:
        dentist (Dentist): The dentist to generate blocks for
        date (datetime.date): The day to generate blocks
        break_minutes (int): optional break between sessions (default 15)
    """
    # Ensure the dentist has a schedule
    try:
        schedule = dentist.schedule
    except DentistSchedule.DoesNotExist:
        raise ValueError(f"Dentist {dentist.full_name} has no schedule set.")

    # Convert times to datetime for calculations
    work_start_dt = datetime.combine(date, schedule.work_start)
    lunch_start_dt = datetime.combine(date, schedule.lunch_start)
    lunch_end_dt = datetime.combine(date, schedule.lunch_end)
    work_end_dt = datetime.combine(date, schedule.work_end)

    current_time = work_start_dt

    blocks_to_create = []

    while current_time < work_end_dt:
        block_end_time = current_time + timedelta(minutes=15)

        # Skip lunch
        if current_time >= lunch_start_dt and current_time < lunch_end_dt:
            current_time = lunch_end_dt
            continue

        # Stop if block exceeds work_end
        if block_end_time > work_end_dt:
            break

        # Check if block already exists
        if not TimeBlock.objects.filter(dentist=dentist, date=date, start_time=current_time.time()).exists():
            blocks_to_create.append(TimeBlock(
                dentist=dentist,
                date=date,
                start_time=current_time.time(),
                end_time=block_end_time.time()
            ))

        # Increment current_time by block duration + break_minutes
        current_time = block_end_time + timedelta(minutes=break_minutes)

    # Bulk create all blocks at once
    TimeBlock.objects.bulk_create(blocks_to_create)
    return f"{len(blocks_to_create)} time blocks generated for {dentist.full_name} on {date}"

