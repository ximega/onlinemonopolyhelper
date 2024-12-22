from typing import Any
from django.core.management.base import BaseCommand
from dashboard.models import CustomUser, INITIAL_BALANCE

class Command(BaseCommand):
    def handle(self, *args: Any, **kwargs: Any) -> None:
        for user in CustomUser.objects.all():
            user.money = INITIAL_BALANCE
            user.last_sent = 0
            user.last_sent_to = "Nobody"
            user.last_received = 0
            user.last_received_from = "Nobody"
            user.last_paid = 0
            user.last_paid_for = "Nothing"
            user.is_billed = False
            user.cur_bill_type = "None"
            user.cur_bill_item = "None"
            user.cur_bill_amount = 0
            user.peak_balance = INITIAL_BALANCE
            user.all_sent = "{}"
            user.all_received = "{}"
            user.largest_bill_paid = 0
            user.bills_paid = 0
            user.save()
        else:
            print("All users' data reset")