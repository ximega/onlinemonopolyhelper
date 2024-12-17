from typing import Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .info import StatsInfo
from onlinemonopolyhelper.info import Info
from dashboard.models import CustomUser

def stats_view(request: HttpRequest) -> HttpResponse:
    peak_balance_user = CustomUser.objects.all().order_by('-peak_balance').first()

    if peak_balance_user is None:
        raise ValueError("peak balances is None")

    ctx: dict[str, Any] = {
        'Info': Info,
        'StatsInfo': StatsInfo,
        'bars': Info.Sidebar.give_other_bars('/stats/', is_staff=request.user.is_staff), # type: ignore
        'player_count': len(CustomUser.objects.all()),
        'wealthiest_player': CustomUser.objects.all().order_by('-money').first(),
        'user': request.user,
        'peak_balance_holder': peak_balance_user.username,
        'peak_balance': peak_balance_user.peak_balance,
        'largest_sent': request.user.get_largest_sent()[1], # type: ignore
        'largest_receiver': request.user.get_largest_sent()[0], # type: ignore
        'largest_received': request.user.get_largest_received()[1], # type: ignore
        'largest_sender': request.user.get_largest_received()[0], # type: ignore
    }

    return render(request, 'stats.html', ctx)