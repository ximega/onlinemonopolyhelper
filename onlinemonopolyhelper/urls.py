"""
URL configuration for onlinemonopolyhelper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from dashboard.views import *
from login.views import *
from cadmin.views import *
from stats.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_dashboard, name='redirect_to_dashboard'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('paybill/', pay_bill, name='pay_bill'),
    path('sendmoney/', send_money, name='send_money'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadmin/', cadmin_view, name='cadmin'),
    path('billplayer/', bill_player, name='bill_player'),
    path('send200/', send_200, name='send_200'),
    path('sendbankmoney/', send_bank_money, name='send_bank_money'),
    path('setbalance/', set_balance, name='set_balance'),
    path('stats/', stats_view, name='stats')
]
