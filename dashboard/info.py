class DashboardInfo:
    cur_balance = "Текущий баланс"
    top_players_title = "Топ игроков"
    player_owes = "должен"
    
    class RecentTransactions:
        title = "Последние транзакции"
        
        class Received:
            title = "Получено"
            suffix = "от"

        class Sent:
            title = "Отправлено"
            suffix = "к"

        class Paid:
            title = "Оплачено"
            suffix = "за"

    class Forms:
        class SendMoney:
            title = "Отправить деньги"
            input_amount = "Сумма"
            input_receiver = "Получатель"
            submit_button = "Отправить"

        class PayBill:
            title = "Оплатить счет"
            amount_placeholder = "Сумма"
            submit_button = "Оплатить"

        class RequestRegionBuy:
            title = "Запросить покупку региона"
            input_region_name = "Регион"
            submit_button = "Запросить"

        class RequestHotelBuild:
            title = "Запросить постройку отеля"
            input_region_name = "Регион"
            input_hotel_count = "Количество"
            submit_button = "Запросить"

        class SellRegion:
            title = "Продать регион банку"
            input_region_name = "Регион"
            submit_button = "Продать"

        class TransferRegion:
            title = "Передать регион"
            input_region_name = "Регион"
            input_receiver_name = "Получатель"
            input_price = "Договоренная цена"
            submit_button = "Отправить"

        class TransferRequest:
            title = "Входящие предложения на закупку регионов"
            region_name = "Регион"
            sender_name = "Отправитель"
            price = "Цена"
            confirm_button = "Принять"
            cancel_button = "Отказать"

    class Errors:
        amount_not_digit = "Вы ввели не числовое значение"
        receiver_does_not_exist = "Получатель не существует"
        not_enough_money = "Недостаточно средств"
        not_valid_amount = "Число должно делиться на 10"