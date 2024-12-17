import json
import logging
from termcolor import colored
from typing import overload
from django.db import models
from django.contrib.auth.models import AbstractUser


INIT_MONEY = 700

type AllCategory = dict[str, int]
type Money = int
type PlayerName = str

class CustomUser(AbstractUser):
    money = models.IntegerField(default=INIT_MONEY)
    last_sent = models.IntegerField(default=0)
    last_sent_to = models.TextField(default="Nobody")
    last_received = models.IntegerField(default=0)
    last_received_from = models.TextField(default="Nobody")
    last_paid = models.IntegerField(default=0)
    last_paid_for = models.TextField(default="Nothing")
    is_billed = models.BooleanField(default=False)
    cur_bill_type = models.TextField(default="None")
    cur_bill_item = models.TextField(default="None")
    cur_bill_amount = models.IntegerField(default=0)
    
    # for statistics
    peak_balance = models.IntegerField(default=INIT_MONEY)
    # player sends
    all_sent = models.TextField(default="{}")
    # player receives
    all_received = models.TextField(default="{}")
    # player pays bill
    largest_bill_paid = models.IntegerField(default=0)
    bills_paid = models.IntegerField(default=0)

    def update_sent(self, amount: int, receiver: str) -> None:
        all_sent: AllCategory = json.loads(self.all_sent)
        if receiver in all_sent.keys():
            all_sent[receiver] += amount
        else:
            all_sent[receiver] = amount
        self.all_sent = json.dumps(all_sent)

    def get_largest_sent(self) -> tuple[PlayerName, Money]:
        all_sent: AllCategory = json.loads(self.all_sent)
        max_sent: int = 0
        if len(all_sent.values()) == 1:
            max_sent = list(all_sent.values())[0]
        elif len(all_sent.values()) > 1:
            max_sent = max(*all_sent.values())
        return (
            {v: k for k, v in all_sent.items()}.get(max_sent, "None"),
            max_sent
        )

    def update_received(self, amount: int, sender: str) -> None:
        all_received: AllCategory = json.loads(self.all_received)
        if sender in all_received.keys():
            all_received[sender] += amount
        else:
            all_received[sender] = amount
        self.all_received = json.dumps(all_received)

    def get_largest_received(self) -> tuple[PlayerName, Money]:
        all_received: AllCategory = json.loads(self.all_received)
        max_received: int = 0
        if len(all_received.values()) == 1:
            max_received = list(all_received.values())[0]
        if len(all_received.values()) > 1:
            max_received = max(*all_received.values())
        return (
            {v: k for k, v in all_received.items()}.get(max_received, "None"),
            max_received
        )
    
    @overload
    def hl_name(self) -> str: ...
    @overload
    def hl_name(self, name: str) -> str: ...
    def hl_name(self, name: str | None = None) -> str:
        if name is None:
            return colored(self.username, 'red', attrs=['bold'])
        return colored(name, 'red', attrs=['bold'])
    
    def logout(self, msg: str) -> None:
        clear_msg: str = msg.replace("[1m[31m", "").replace("[0m", "")
        logging.info(clear_msg)
    
    def pay_bill(self) -> None:
        self.logout(f'{self.hl_name()} payed of its bill on ${self.cur_bill_amount}')
        if self.cur_bill_amount > self.largest_bill_paid:
            self.largest_bill_paid = self.cur_bill_amount
        self.bills_paid += 1
        self.last_paid = self.cur_bill_amount
        self.last_paid_for = f"{self.cur_bill_item} ({self.cur_bill_type})"
        self.money -= self.cur_bill_amount
        self.cur_bill_amount = 0
        self.cur_bill_type = "None"
        self.cur_bill_item = "None"
        self.is_billed = False
        self.save()

    def send_bill(self, bill_type: str, bill_item: str, amount: int) -> None:
        self.is_billed = True
        self.cur_bill_type = bill_type
        self.cur_bill_item = bill_item
        self.cur_bill_amount = amount
        self.save()
        self.logout(f'{self.hl_name()} received a bill on {bill_type} with {bill_item} at ${amount}')

    def send_money(self, amount: int, receiver_str: str) -> None:
        self.money -= amount
        self.last_sent = amount
        self.last_sent_to = receiver_str
        self.update_sent(amount, receiver_str)
        self.save()
        self.logout(f'{self.hl_name()} sent ${amount} to {self.hl_name(receiver_str)}')

    def receive_money(self, amount: int, sender_str: str) -> None:
        self.money += amount
        if self.money > self.peak_balance:
            self.peak_balance = self.money
        self.last_received = amount
        self.last_received_from = sender_str
        self.update_received(amount, sender_str)
        self.save()
        self.logout(f'{self.hl_name()} received ${amount} from {self.hl_name(sender_str)}')