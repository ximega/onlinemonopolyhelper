from typing import Any
from django.core.management.base import BaseCommand
from dashboard.models import CustomUser

class Command(BaseCommand):
    def handle(self, *args: Any, **kwargs: Any) -> None:
        user = CustomUser.objects.create_user(username=input('Nickname: '), password=input('Password: '), email='')
        user.save()
        print(f'{user.username} added to db')