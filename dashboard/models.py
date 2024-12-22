import json
import logging
import os
from termcolor import colored
from typing import overload, Any
from django.db import models
from django.contrib.auth.models import AbstractUser


GAMES_PATH = os.path.join(os.getcwd(), 'games')
GAMES_MAIN_DATA_PATH = os.path.join(GAMES_PATH, 'data.json')

def ask_to_choose_game_type(game_types: Any) -> str:
    msg = "Choose of the following game types to continue:\n"
    for index, game_k in enumerate(game_types.keys(), start=1):
        msg += f"{index}) {game_k}"
    print(msg)
    inp: str = input()
    while not inp.isdigit():
        print('Enter a number!')
        inp = input()
    return game_types[list(game_types.keys())[int(inp)-1]]['path']

def read_main_data() -> Any:
    return json.loads(open(GAMES_MAIN_DATA_PATH, 'r').read())

def get_chosen_type_path() -> str:
    data = read_main_data()
    chosen_type_path: str = data['chosen_type_path']
    if chosen_type_path == "":
        chosen_type_path = ask_to_choose_game_type(data['game_types'])
        wfile = open(GAMES_MAIN_DATA_PATH, 'w')
        data['chosen_type_path'] = chosen_type_path
        wfile.write(json.dumps(data, indent=4))
    return os.path.join(GAMES_PATH, chosen_type_path)

def get_all_regions_list(path: str) -> list[str]:
    return json.loads(open(os.path.join(path, 'regions', 'list.json'), 'r').read())

def get_regions_buy_prices(path: str) -> dict[str, int]:
    return json.loads(open(os.path.join(path, 'regions', 'buy.json'), 'r').read())

def get_regions_hotel_prices(path: str) -> dict[str, int]:
    return json.loads(open(os.path.join(path, 'regions', 'hotels.json'), 'r').read())

def get_initial_balance(path: str) -> int:
    data = json.loads(open(os.path.join(path, 'data.json'), 'r').read())
    return data['initial_balance']

def get_max_hotel_count(path: str) -> str:
    data = json.loads(open(os.path.join(path, 'data.json'), 'r').read())
    return data['max_hotels_on_region']

def get_bought_regions() -> list[str]:
    data = read_main_data()
    return data['bought_regions']

def add_bought_region(region_name: str) -> None:
    data = read_main_data()
    data['bought_regions'].append(region_name)
    wfile = open(GAMES_MAIN_DATA_PATH, 'w')
    wfile.write(json.dumps(data))

def remove_bought_region(region_name: str) -> None:
    data = read_main_data()
    data['bought_regions'].remove(region_name)
    wfile = open(GAMES_MAIN_DATA_PATH, 'w')
    wfile.write(json.dumps(data))

CHOSEN_TYPE_PATH: str = get_chosen_type_path()
REGIONS_LIST: list[str] = get_all_regions_list(CHOSEN_TYPE_PATH)
REGIONS_BUY_PRICES: dict[str, int] = get_regions_buy_prices(CHOSEN_TYPE_PATH)
REGIONS_HOTEL_PRICES: dict[str, int] = get_regions_hotel_prices(CHOSEN_TYPE_PATH)
INITIAL_BALANCE = get_initial_balance(CHOSEN_TYPE_PATH)
MAX_HOTEL_COUNT = get_max_hotel_count(CHOSEN_TYPE_PATH)

type AllCategory = dict[str, int]
type Money = int
type PlayerName = str

class CustomUser(AbstractUser):
    money = models.IntegerField(default=INITIAL_BALANCE)
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
    peak_balance = models.IntegerField(default=INITIAL_BALANCE)
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

class RegionBuyRequest(models.Model):
    region_name = models.TextField()
    sent_by = models.TextField()

    def __str__(self) -> str:
        return f"{self.region_name} - {self.sent_by}"

class HotelBuildRequest(models.Model):
    region_name = models.TextField()
    sent_by = models.TextField()
    count = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.region_name} - {self.sent_by} - {self.count}"