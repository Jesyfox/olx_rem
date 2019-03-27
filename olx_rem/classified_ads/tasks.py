from __future__ import absolute_import, unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from .models import Item

from datetime import timedelta
from django.utils.timezone import now


# if new_test.cleaned_data['delay'] == MINUTES:
#     minutes = int(new_test.cleaned_data['count'])
#     time_to_exp = now() + timedelta(minutes=minutes)
#     delete_test.apply_async((named_test.id,), eta=time_to_exp)
#
# elif new_test.cleaned_data['delay'] == DAYS:
#     days = int(new_test.cleaned_data['count'])
#     time_to_exp = now() + timedelta(days=days)
#     delete_test.apply_async((named_test.id,), eta=time_to_exp)

@shared_task
def delete_item(id=None):
    if id is None:
        return None
    try:
        Item.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        return 'object does not exist!'
    return 'delete is done!'
