from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from dashboard.models import CustomUser, RegionBuyRequest, HotelBuildRequest, REGIONS_BUY_PRICES, REGIONS_HOTEL_PRICES
from onlinemonopolyhelper.info import Info
from .info import CAdminInfo

def cadmin_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        return redirect('/cadmin/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    if not request.user.is_staff: # type: ignore
        return redirect('/dashboard/')
    
    ctx = {
        'Info': Info,
        'CAdminInfo': CAdminInfo,
        'bars': Info.Sidebar.give_other_bars('/cadmin/', is_staff=True), # type: ignore
        'users': CustomUser.objects.all().order_by('-money'),
        'buyrequests': RegionBuyRequest.objects.all(),
        'buildrequests': HotelBuildRequest.objects.all(),
    }

    return render(request, 'cadmin.html', ctx)

def bill_player(request: HttpRequest) -> HttpResponse: 
    if request.method != "POST":
        return redirect('/cadmin/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    bill_type = request.POST.get('type')
    bill_item = request.POST.get('item')
    bill_amount_str = request.POST.get('amount')
    bill_receiver_name = request.POST.get('receiver')

    if bill_amount_str is None or bill_item is None or bill_type is None or bill_receiver_name is None:
        raise ValueError(f"One of amount or receiver_name is None: {bill_type=}, {bill_item=}, {bill_amount_str=}, {bill_receiver_name=}")
    
    if not bill_amount_str.isdigit():
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.amount_not_digit})
    
    bill_amount = int(bill_amount_str)

    if bill_amount % 10 > 0:
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.not_valid_amount})
    
    try:
        bill_receiver = CustomUser.objects.get(username=bill_receiver_name)

        if bill_receiver.is_billed:
            return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.receiver_already_billed})
        
        bill_receiver.send_bill(bill_type, bill_item, bill_amount)

        return redirect('/cadmin/')
    
    except CustomUser.DoesNotExist:
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.receiver_does_not_exist})
    
def send_bank_money(request: HttpRequest) -> HttpResponse: 
    if request.method != "POST":
        return redirect('/cadmin/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    amount_str = request.POST.get('amount')
    player_name = request.POST.get('player')

    if amount_str is None or player_name is None:
        raise ValueError(f"One of amount_str or player_name is None: {amount_str=}, {player_name=}")
    
    if not amount_str.isdigit():
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.amount_not_digit})
    
    amount = int(amount_str)

    if amount % 10 > 0:
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.not_valid_amount})
    
    try:
        player = CustomUser.objects.get(username=player_name)

        player.receive_money(amount, CAdminInfo.SendBankMoney.received_from_bank)

        return redirect('/cadmin/')

    except CustomUser.DoesNotExist:
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.receiver_does_not_exist})
    
def send_200(request: HttpRequest) -> HttpResponse: 
    if request.method != "POST":
        return redirect('/cadmin/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    player_name = request.POST.get('player')
    
    try:
        player = CustomUser.objects.get(username=player_name)

        player.receive_money(200, CAdminInfo.SendBankMoney.received_from_bank)

        return redirect('/cadmin/')

    except CustomUser.DoesNotExist:
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.receiver_does_not_exist})
    
def set_balance(request: HttpRequest) -> HttpResponse: 
    if request.method != "POST":
        return redirect('/cadmin/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    amount_str = request.POST.get('amount')
    player_name = request.POST.get('player')

    if amount_str is None or player_name is None:
        raise ValueError(f"One of amount_str or player_name is None: {amount_str=}, {player_name=}")
    
    if not amount_str.isdigit():
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.amount_not_digit})
    
    amount = int(amount_str)

    if amount % 10 > 0:
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.not_valid_amount})
    
    try:
        player = CustomUser.objects.get(username=player_name)

        player.money = amount
        player.save()
        player.logout(f'{player.hl_name()}\'s balance was set to {amount}')

        return redirect('/cadmin/')

    except CustomUser.DoesNotExist:
        return render(request, 'blankpage.html', {'alert_msg': CAdminInfo.Errors.receiver_does_not_exist})
    
def cancel_buy_region(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/cadmin/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    request_id = int(request.POST.get('request_id')) # type: ignore
    buy_request = RegionBuyRequest.objects.get(id=request_id)
    user = CustomUser.objects.get(username=buy_request.sent_by)

    user.logout(f"{user.hl_name()}'s request to buy a region {buy_request.region_name} was cancelled")

    buy_request.delete()

    return redirect('/cadmin/')
    
def cancel_build_hotel(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/cadmin/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    request_id = int(request.POST.get('request_id')) # type: ignore
    build_request = HotelBuildRequest.objects.get(id=request_id)
    user = CustomUser.objects.get(username=build_request.sent_by)

    user.logout(f"{user.hl_name()}'s request to build a hotel in a region {build_request.region_name} was cancelled")

    build_request.delete()

    return redirect('/cadmin/')
    
def confirm_buy_region(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/cadmin/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')

    request_id = int(request.POST.get('request_id')) # type: ignore
    buy_request = RegionBuyRequest.objects.get(id=request_id)
    user = CustomUser.objects.get(username=buy_request.sent_by)

    user.money -= REGIONS_BUY_PRICES[buy_request.region_name]
    user.save()

    user.logout(f"{user.hl_name()} has bought a region {buy_request.region_name}")
    
    buy_request.delete()

    return redirect('/cadmin/')

def confirm_build_hotel(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/cadmin/')
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    request_id = int(request.POST.get('request_id')) # type: ignore
    build_request = HotelBuildRequest.objects.get(id=request_id)
    user = CustomUser.objects.get(username=build_request.sent_by)

    user.money -= REGIONS_HOTEL_PRICES[build_request.region_name] * build_request.count
    user.save()

    user.logout(f"{user.hl_name()} has built {build_request.count} hotel(-s) in a region {build_request.region_name}")

    build_request.delete()

    return redirect('/cadmin/')