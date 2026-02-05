from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DentistSchedule
from .utils import generate_time_blocks_for_dentist
from datetime import date, timedelta

@receiver(post_save, sender=DentistSchedule)
def create_time_blocks_on_schedule(sender, instance, created, **kwargs):
    """
    Triggered when a new DentistSchedule is created.
    Generates TimeBlocks for today and the next 30 days.
    """
    if created:
        dentist = instance.dentist
        today = date.today()
        # Generate blocks for today + next 30 days
        for i in range(0, 31):  # 0 = today, 1-30 = next 30 days
            generate_time_blocks_for_dentist(dentist, today + timedelta(days=i))
