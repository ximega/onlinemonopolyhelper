from typing import Literal


class Info:
    class Header:
        title = "Помощник монополии"
        logout = "Выйти"

    class Sidebar:
        class Dashboard:
            text = 'Главная'
            ref = '/dashboard/'

        class Admin:
            text = 'Панель админа'
            ref = '/admin/'

        class CAdmin:
            text = 'Игровая админка'
            ref = '/cadmin/'

        class Stats:
            text = 'Статистика'
            ref = '/stats/'

        @staticmethod
        def make_href(text: str, ref: str) -> str:
            return f'<a href="{ref}">{text}</a>'

        @classmethod
        def give_other_bars(cls, cur: str, *, is_staff: Literal[True] | None = None) -> list[str]:
            pairs = {
                '/dashboard/': [cls.Admin, cls.CAdmin, cls.Stats],
                '/admin/': [cls.Dashboard, cls.CAdmin, cls.Stats],
                '/cadmin/': [cls.Dashboard, cls.Admin, cls.Stats],
                '/stats/': [cls.Dashboard, cls.Admin, cls.CAdmin]
            }

            bars: list[str] = []
            for bar in pairs[cur]:
                if (not is_staff) and (bar in (cls.Admin, cls.CAdmin)):
                    continue
                bars.append(cls.make_href(bar.text, bar.ref))

            return bars