class CAdminInfo:
    class Errors:
        amount_not_digit = "Вы ввели не числовое значение"
        receiver_does_not_exist = "Получатель не существует"
        not_valid_amount = "Число должно делиться на 10"
        receiver_already_billed = "Получать счета уже имеет счет и не может получить второй пока не оплатит первый"

    class Requests:
        class BuyRegion:
            title = "Запросы на покупку региона"
            region_name = "Название региона"
            sent_by = "Отправлен"

        class BuildHotel:
            title = "Запросы на постройку отелей"
            region_name = "Название региона"
            sent_by = "Отправлен"
            count = "Количество отелей"

        class TransferRegion:
            title = "Запросы на передачу регионов"
            region_name = "Название региона"
            sender_name = "Отправитель"
            receiver_name = "Получатель"
            price = "Договоренная цена"

        confirm_button = "Подтвердить"
        cancel_button = "Отказать"

    class SendBill:
        title = "Выставить счет"

        class BillType:
            title = "Тип"
            first_select_option = "Выберите тип"
            types: list[str] = [
                'Штраф',
            ]

        item_title = "Предмет"

        amount_title = "Сумма"

        class BillReceiver:
            title = "Получатель"
            first_select_option = "Выберите игрока"
            
        submit_button = "Отправить счет"

    class SendBankMoney:
        received_from_bank = "Банка"
        title = "Отправить деньги банка"
        amount_title = "Сумма"

        class Player:
            title = "Получатель"
            first_select_option = "Выберите игрока"
        
        submit_button = "Отправить деньги"

    class Send200:
        title = "Отправить за поле вперед"

        class Player:
            title = "Получатель"
            first_select_option = "Выберите игрока"
        
        submit_button = "Отправить деньги"

    class SetBalance:
        title = "Установить баланс игрока"
        amount_title = "Новая сумма"

        class Player:
            title = "Игрок"
            first_select_option = "Выберите игрока"

        submit_button = "Установить баланс"