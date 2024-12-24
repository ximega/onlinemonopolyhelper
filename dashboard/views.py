from typing import Any
from django.contrib.auth.models import UserManager
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from onlinemonopolyhelper.info import Info
from .info import DashboardInfo
from .models import (
    CustomUser, RegionBuyRequest, HotelBuildRequest, TransferRegionRequest,
    REGIONS_LIST, MAX_HOTEL_COUNT, REGIONS_BUY_PRICES, REGIONS_HOTEL_PRICES, CHOSEN_TYPE_PATH,
    remove_bought_region, get_bought_regions, get_all_regions_list,
)

def dashboard_view(request: HttpRequest) -> HttpResponse: 
    if request.method == "POST":
        return redirect('/dashboard/')

    if not request.user.is_authenticated:
        return redirect('/login/')
    
    top_players: UserManager[CustomUser] = CustomUser.objects.all().order_by('-money')

    ctx: dict[str, Any] = {
        'Info': Info,
        'DashboardInfo': DashboardInfo,
        'bars': Info.Sidebar.give_other_bars('/dashboard/', is_staff=request.user.is_staff), # type: ignore
        'user': request.user,
        'top_players': top_players,
        'other_players': [player for player in top_players if player.username != request.user.username], # type: ignore
        'regions': REGIONS_LIST,
        'max_hotel_count': MAX_HOTEL_COUNT,
        'user_regions': request.user.get_regions(), # type: ignore
        'user_regions_plain': "\n".join(request.user.get_regions()), # type: ignore
        'available_regions': list(set(get_all_regions_list(CHOSEN_TYPE_PATH)) - set(get_bought_regions())),
        'incoming_transfer_requests': TransferRegionRequest.objects.filter(receiver__icontains=request.user.username, approved_by_receiver=False) # type: ignore
    }
    
    return render(request, 'dashboard.html', ctx)

def redirect_to_dashboard(request: HttpRequest) -> HttpResponse:
    return redirect('/dashboard/')

def send_money(request: HttpRequest) -> HttpResponse: 
    if request.method != "POST":
        return redirect('/dashboard/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    amount_str: str = request.POST.get('amount') # type: ignore
    receiver_name: str = request.POST.get('receiver_name') # type: ignore
    
    if not amount_str.isdigit():
        return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.amount_not_digit})

    amount = int(amount_str)

    if amount % 10 > 0:
        return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.not_valid_amount})

    try:
        receiver: CustomUser = CustomUser.objects.get(username=receiver_name)

        if request.user.money - amount < 0: # type: ignore
            return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.not_enough_money})
        
        request.user.send_money(amount, receiver.username) # type: ignore

        receiver.receive_money(amount, request.user.username) # type: ignore

        return redirect('/dashboard/')

    except CustomUser.DoesNotExist:
        return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.receiver_does_not_exist})

def pay_bill(request: HttpRequest) -> HttpResponse: 
    if request.method != "POST":
        return redirect('/dashboard/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    if request.user.money < request.user.cur_bill_amount: # type: ignore
        return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.not_enough_money})
    
    request.user.pay_bill() # type: ignore

    return redirect('/dashboard/')

def request_region_buy(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/dashboard/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    region_name: str = request.POST.get('region_name') # type: ignore

    if request.user.money < REGIONS_BUY_PRICES[region_name]: # type: ignore
        return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.not_enough_money})

    buy_request = RegionBuyRequest(region_name=region_name, sent_by=request.user.username) # type: ignore
    buy_request.save()

    return redirect('/dashboard/')
    
def request_hotel_build(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/dashboard/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    region_name: str = request.POST.get('region_name') # type: ignore
    hotel_count = int(request.POST.get('hotel_count')) # type: ignore

    if request.user.money < REGIONS_HOTEL_PRICES[region_name] * hotel_count: # type: ignore
        return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.not_enough_money})

    build_request = HotelBuildRequest(region_name=region_name, sent_by=request.user.username, count=hotel_count) # type: ignore
    build_request.save()

    return redirect('/dashboard/')

def sell_region(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/dashboard/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    region_name: str = request.POST.get('region_name') # type: ignore

    price: int = REGIONS_BUY_PRICES[region_name]

    user: CustomUser = request.user # type: ignore

    user.money += price
    user.remove_region(region_name)
    remove_bought_region(region_name)
    user.save()

    return redirect('/dashboard/')

def transfer_region(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/dashboard/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    region_name: str = request.POST.get('region_name') # type: ignore
    receiver_name: str = request.POST.get('receiver_name') # type: ignore
    sender_name: str = request.user.username # type: ignore
    price = int(request.POST.get('price')) # type: ignore

    receiver: CustomUser = CustomUser.objects.get(username=receiver_name)

    if receiver.money < price:
        return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.not_enough_money})

    if price % 10 != 0:
        return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.not_valid_amount})

    TransferRegionRequest(region_name=region_name, 
                          receiver=receiver_name, 
                          sender=sender_name, 
                          price=price, 
                          approved_by_receiver=False).save()
    
    return redirect('/dashboard/')

def user_confirm_transfer_request(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/dashboard/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    request_id = int(request.POST.get('request_id')) # type: ignore

    transfer_request: TransferRegionRequest = TransferRegionRequest.objects.get(id=request_id)
    transfer_request.approved_by_receiver = True
    transfer_request.save()

    return redirect('/dashboard/')

def user_cancel_transfer_request(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/dashboard/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    request_id = int(request.POST.get('request_id')) # type: ignore

    TransferRegionRequest.objects.get(id=request_id).delete()

    return redirect('/dashboard/')