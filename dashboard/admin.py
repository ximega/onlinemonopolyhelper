from django.contrib import admin

from .models import CustomUser, RegionBuyRequest, HotelBuildRequest, TransferRegionRequest

admin.site.register(CustomUser)
admin.site.register(RegionBuyRequest)
admin.site.register(HotelBuildRequest)
admin.site.register(TransferRegionRequest)