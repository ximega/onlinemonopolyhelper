from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .info import LoginInfo
from onlinemonopolyhelper.info import Info

@csrf_exempt
def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    ctx: dict[str, Any] = {
        'Info': Info,
        'LoginInfo': LoginInfo
    }
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            raise ValueError(f"One of username or password is None: {username=}, {password=}")
        
        username = username.strip().lower()
        password = password.strip().lower()

        user = authenticate(request, username=username, password=password)
        
        if user is None:
            messages.error(request, LoginInfo.Errors.invalid_data)
            return render(request, 'login.html', ctx)
        
        login(request, user)
        return redirect('/')

    return render(request, 'login.html', ctx)

@csrf_exempt
def logout_view(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect('/dashboard/')

    logout(request)
    return redirect('/dashboard/')