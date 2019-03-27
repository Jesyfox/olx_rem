from django.utils.timezone import now

from datetime import timedelta


def get_task_execute_delay():
    DAYS_UNTIL_DELETE = 30

    return now() + timedelta(days=DAYS_UNTIL_DELETE)
