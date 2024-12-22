from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from onlinemonopolyhelper.info import Info
from .info import DashboardInfo
from .models import CustomUser, RegionBuyRequest, HotelBuildRequest, REGIONS_LIST, MAX_HOTEL_COUNT, REGIONS_BUY_PRICES, REGIONS_HOTEL_PRICES

def dashboard_view(request: HttpRequest) -> HttpResponse: 
    if request.method == "POST":
        return redirect('/dashboard/')

    if not request.user.is_authenticated:
        return redirect('/login/')
    
    top_players = CustomUser.objects.all().order_by('-money')

    ctx: dict[str, Any] = {
        'Info': Info,
        'DashboardInfo': DashboardInfo,
        'bars': Info.Sidebar.give_other_bars('/dashboard/', is_staff=request.user.is_staff), # type: ignore
        'user': request.user,
        'top_players': top_players,
        'other_players': [player for player in top_players if player.username != request.user.username], # type: ignore
        'regions': REGIONS_LIST,
        'max_hotel_count': MAX_HOTEL_COUNT,
    }
    
    return render(request, 'dashboard.html', ctx)

def redirect_to_dashboard(request: HttpRequest) -> HttpResponse:
    return redirect('/dashboard/')

def send_money(request: HttpRequest) -> HttpResponse: 
    if request.method != "POST":
        return redirect('/dashboard/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    amount_str = request.POST.get('amount')
    receiver_name = request.POST.get('receiver_name')

    if amount_str is None or receiver_name is None:
        raise ValueError(f"One of amount or receiver_name is None: {amount_str=}, {receiver_name=}")
    
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
    
    region_name = request.POST.get('region_name')

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
    
    region_name = request.POST.get('region_name')
    hotel_count = int(request.POST.get('hotel_count')) # type: ignore

    if request.user.money < REGIONS_HOTEL_PRICES[region_name] * hotel_count: # type: ignore
        return render(request, 'blankpage.html', {'alert_msg': DashboardInfo.Errors.not_enough_money})

    build_request = HotelBuildRequest(region_name=region_name, sent_by=request.user.username, count=hotel_count) # type: ignore
    build_request.save()

    return redirect('/dashboard/')

