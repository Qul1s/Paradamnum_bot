import telebot
import configure
from telebot import types
import balanceController
import datetime
from datetime import datetime
import chart
import urllib.request


client = telebot.TeleBot(configure.config['token'])

@client.message_handler(commands = ['operation'])
def get_user_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_add = types.InlineKeyboardButton(text = 'Доход', callback_data = 'Add')
    item_expense = types.InlineKeyboardButton(text='Расход', callback_data='Expense')
    markup_inline.add(item_add, item_expense)
    client.send_message(message.chat.id, 'Выбери действие, будущий олигарх', reply_markup= markup_inline)

@client.callback_query_handler(func=lambda call:True)
def answer(call):
    ##Запись
        if call.data == 'Add':
            msg = client.send_message(call.message.chat.id, 'Сколько же ты заработал, мой милый друг?\nФормат: Сумма, Категория')
            client.register_next_step_handler(msg, change_balance, call)
        elif call.data == 'Expense':
            msg = client.send_message(call.message.chat.id, 'Какая сумма была потрачена?\nФормат: Сумма, Категория')
            client.register_next_step_handler(msg, change_balance, call)

    ##Доходы
        elif call.data == 'December':
            month_earnings(call.message.chat.id, '12', 'Декабрь: ')
        elif call.data == 'November':
            month_earnings(call.message.chat.id, '11', 'Ноябрь: ')
        elif call.data == 'October':
            month_earnings(call.message.chat.id, '10', 'Октябрь: ')
        elif call.data == 'September':
            month_earnings(call.message.chat.id, '09', 'Сентябрь: ')
        elif call.data == 'August':
            month_earnings(call.message.chat.id, '08', 'Август: ')
        elif call.data == 'July':
            month_earnings(call.message.chat.id, '07', 'Июль: ')
        elif call.data == 'June':
            month_earnings(call.message.chat.id, '06', 'Июнь: ')
        elif call.data == 'May':
            month_earnings(call.message.chat.id, '05', 'Май: ')
        elif call.data == 'April':
            month_earnings(call.message.chat.id, '04', 'Апрель: ')
        elif call.data == 'March':
            month_earnings(call.message.chat.id, '03', 'Март: ')
        elif call.data == 'February':
            month_earnings(call.message.chat.id, '02', 'Февраль: ')
        elif call.data == 'January':
            month_earnings(call.message.chat.id, '01', 'Январь: ')

    ##Расходы
        elif call.data == 'December_expense':
            month_expenses(call.message.chat.id, '12', 'Декабрь: ')
        elif call.data == 'November_expense':
            month_expenses(call.message.chat.id, '11', 'Ноябрь: ')
        elif call.data == 'October_expense':
            month_expenses(call.message.chat.id, '10', 'Октябрь: ')
        elif call.data == 'September_expense':
            month_expenses(call.message.chat.id, '09', 'Сентябрь: ')
        elif call.data == 'August_expense':
            month_expenses(call.message.chat.id, '08', 'Август: ')
        elif call.data == 'July_expense':
            month_expenses(call.message.chat.id, '07', 'Июль: ')
        elif call.data == 'June_expense':
            month_expenses(call.message.chat.id, '06', 'Июнь: ')
        elif call.data == 'May_expense':
            month_expenses(call.message.chat.id, '05', 'Май: ')
        elif call.data == 'April_expense':
            month_expenses(call.message.chat.id, '04', 'Апрель: ')
        elif call.data == 'March_expense':
            month_expenses(call.message.chat.id, '03', 'Март: ')
        elif call.data == 'February_expense':
            month_expenses(call.message.chat.id, '02', 'Февраль: ')
        elif call.data == 'January_expense':
            month_expenses(call.message.chat.id, '01', 'Январь: ')

        else:
            client.send_message(call.message.chat.id, 'Где-то случилась ошибка')


##Показаль баланс
@client.message_handler(commands = ['balance'])
def get_balance(message):
    currentbalance = str(balanceController.current_balance(message.from_user.id))
    client.send_message(message.chat.id, 'Твой баланс: ' + currentbalance)

##Вывести все категории дохода
@client.message_handler(commands = ['mycategoryearnings'])
def output_all_add_category(message):
    output_all_category_earnings = str(balanceController.output_all_add_category(message.from_user.id))
    output = str(output_all_category_earnings).replace("[","").replace("'", "").replace("]","").replace(",", "").replace("(", "").replace(") ", ", ").replace(")", " ")
    client.send_message(message.chat.id, 'Твои категории дохода:\n' + output)
##Вывести все категории расходов
@client.message_handler(commands = ['mycategoryexpense'])
def output_all_expense_category(message):
    output_all_category_expense = str(balanceController.output_all_expense_category(message.from_user.id))
    output = str(output_all_category_expense).replace("[", "").replace("'", "").replace("]", "").replace(",", "").replace("(","").replace(") ", ", ").replace(")", " ")
    client.send_message(message.chat.id, 'Твои категории расхода:\n' + output)
##Вывести все доходы
@client.message_handler(commands = ['allearnings'])
def all_earnings(message):
    all_earnings = balanceController.output_all_earnings(message.from_user.id)
    if len(all_earnings) == 0:
        client.send_message(message.chat.id, 'Вы еще не вносили ваш доход\nСделать это можно с помощью команды /operation')
    else:
        earnings = []
        for i in all_earnings:
            category = "\nКатегория: " + str(i[0])
            value = "\nСумма: " + str(i[1])
            date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m | %H:%M | %a') + '\n'
            all = category + value + date
            earnings.append(all)

        category_array = balanceController.output_all_add_category(message.chat.id)
        value_array = balanceController.output_sum_earnings_groupby_category(message.chat.id)
        url = chart.draw_chart(category_array, value_array)
        img = urllib.request.urlopen(url).read()
        all_earnings_sum = str(balanceController.current_all_earnings(message.chat.id))
        text = '\nВсего заработано: ' + all_earnings_sum + "\nВсе твои доходы: " +  str(earnings).replace("[","").replace("'", "").replace("]","").replace(",", "").replace("\\n", "\n")
        client.send_photo(message.chat.id, img, text)
##Вывести все расходы
@client.message_handler(commands = ['allexpenses'])
def all_expense(message):
    all_expense = balanceController.output_all_expense(message.from_user.id)
    if len(all_expense) == 0:
        client.send_message(message.chat.id, 'Вы еще не вносили ваши расходы\nСделать это можно с помощью команды /operation')
    else:
        expense = []
        for i in all_expense:
            category = "\nКатегория: " + str(i[0])
            value = "\nСумма: " + str(i[1])
            date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m | %H:%M | %a')
            all = category + value + date
            expense.append(all)

        category_array = balanceController.output_all_expense_category(message.chat.id)
        value_array = balanceController.output_sum_expense_groupby_category(message.chat.id)
        all_expense_sum = str(balanceController.current_all_expense(message.chat.id))
        url = chart.draw_chart(category_array, value_array)
        img = urllib.request.urlopen(url).read()
        text = '\nВсего потрачено: ' + all_expense_sum + "\nВсе твои расходы:"+  str(expense).replace("[","").replace("'", "").replace("]","").replace(",", "").replace("\\n", "\n")
        client.send_photo(message.chat.id, img, text)
##Вывести все доходы за определённый месяц
@client.message_handler(commands = ['earningsmonth'])
def earnings_month(message):
    if check_for_subsribe(message.chat.id) == True:
        markup_inline = types.InlineKeyboardMarkup()
        item_January = types.InlineKeyboardButton(text='Январь', callback_data='January')
        item_February = types.InlineKeyboardButton(text='Февраль', callback_data='February')
        item_March = types.InlineKeyboardButton(text='Март', callback_data='March')
        item_April = types.InlineKeyboardButton(text='Апрель', callback_data='April')
        item_May = types.InlineKeyboardButton(text='Май', callback_data='May')
        item_June = types.InlineKeyboardButton(text='Июнь', callback_data='June')
        item_July = types.InlineKeyboardButton(text='Июль', callback_data='July')
        item_August = types.InlineKeyboardButton(text='Август', callback_data='August')
        item_September = types.InlineKeyboardButton(text='Сентябрь', callback_data='September')
        item_October = types.InlineKeyboardButton(text='Октябрь', callback_data='October')
        item_November = types.InlineKeyboardButton(text='Ноябрь', callback_data='November')
        item_December = types.InlineKeyboardButton(text='Декабрь', callback_data='December')
        markup_inline.add(item_January, item_February, item_March, item_April, item_May, item_June, item_July, item_August, item_September, item_October, item_November, item_December)
        client.send_message(message.chat.id, 'Выберите месяц, мой господин', reply_markup=markup_inline)
    else:
        client.send_message(message.chat.id, 'У вас нет доступа к этой команде\nКупить подписку можно командой\n/subscription')
##Вывести все расходы за определенный месяц
@client.message_handler(commands = ['expensesmonth'])
def expenses_month(message):
    if check_for_subsribe(message.chat.id) == True:
        markup_inline = types.InlineKeyboardMarkup()
        item_January1 = types.InlineKeyboardButton(text='Январь', callback_data='January_expense')
        item_February = types.InlineKeyboardButton(text='Февраль', callback_data='February_expense')
        item_March = types.InlineKeyboardButton(text='Март', callback_data='March_expense')
        item_April = types.InlineKeyboardButton(text='Апрель', callback_data='April_expense')
        item_May = types.InlineKeyboardButton(text='Май', callback_data='May_expense')
        item_June = types.InlineKeyboardButton(text='Июнь', callback_data='June_expense')
        item_July = types.InlineKeyboardButton(text='Июль', callback_data='July_expense')
        item_August = types.InlineKeyboardButton(text='Август', callback_data='August_expense')
        item_September = types.InlineKeyboardButton(text='Сентябрь', callback_data='September_expense')
        item_October = types.InlineKeyboardButton(text='Октябрь', callback_data='October_expense')
        item_November = types.InlineKeyboardButton(text='Ноябрь', callback_data='November_expense')
        item_December = types.InlineKeyboardButton(text='Декабрь', callback_data='December_expense')
        markup_inline.add(item_January1, item_February, item_March, item_April, item_May, item_June, item_July, item_August, item_September, item_October, item_November, item_December)
        client.send_message(message.chat.id, 'Выберите месяц, мой господин', reply_markup=markup_inline)
    else:
        client.send_message(message.chat.id,
                            'У вас нет доступа к этой команде\nКупить подписку можно командой\n/subscription')

@client.message_handler(commands = ['earningscategory'])
def categoryearnings(message):
    if check_for_subsribe(message.chat.id) == True:
        output_all_category = str(balanceController.output_all_add_category(message.from_user.id))
        output = str(output_all_category).replace("[", "").replace("'", "").replace("]", "").replace(",", "").replace("(",
                                                                                                                      "").replace(
            ") ", ", ").replace(")", " ")
        client.send_message(message.chat.id, 'Введите категорию\nТвои категории дохода:\n' + output)
        client.register_next_step_handler(message, category_earnings)
    else:
        client.send_message(message.chat.id,
                            'У вас нет доступа к этой команде\nКупить подписку можно командой\n/subscription')

@client.message_handler(commands = ['expensecategory'])
def categoryexpense(message):
    if check_for_subsribe(message.chat.id) == True:
        output_all_category = str(balanceController.output_all_expense_category(message.from_user.id))
        output = str(output_all_category).replace("[", "").replace("'", "").replace("]", "").replace(",", "").replace("(",
                                                                                                                      "").replace(
            ") ", ", ").replace(")", " ")
        client.send_message(message.chat.id, 'Введите категорию\nТвои категории расхода:\n' + output)
        client.register_next_step_handler(message, category_expense)
    else:
        client.send_message(message.chat.id,
                            'У вас нет доступа к этой команде\nКупить подписку можно командой\n/subscription')

##Старт
@client.message_handler(commands = ['start'])
def start(message):
        balanceController.new_user(message.from_user.id)
        photo = open('paradamnumprew.png', 'rb')
        text = 'Привет, я бот, который поможет тебе контролировать твои денежные ресурсы!😎 \nТвой ID: ' + str(message.from_user.id)
        client.send_photo(message.chat.id, photo, text)
##Разработчики
@client.message_handler(commands = ['developers'])
def start(message):
        client.send_message(message.chat.id, 'Бот был создан: @retiunskykh')
##Подписка
@client.message_handler(commands = ['subscription'])
def start(message):
    subsribetime = datetime.strptime(balanceController.output_subscribe_time(message.chat.id), "%Y-%m-%d %H:%M:%S")
    if check_for_subsribe(message.chat.id) == True:
        client.send_message(message.chat.id, 'У вас есть подписка, которая действует до: ' + str(subsribetime.strftime('%Y-%m-%d')))
    elif check_for_subsribe(message.chat.id) == False:
        client.send_message(message.chat.id, 'У вас нет подписки\nЧтобы купить подписку выберите тариф снизу\nДо 6 месяцев - 99 рублей/месяц\n6 месяцев - 499 рублей\n1 год - 999 рублей\nИ оплатите заданную сумму на карту: 4441 1144 1244 6062\nВ комментариях указать свой ID: '+ str(message.chat.id))
##АдминПанель
@client.message_handler(commands = ['adminpanel'])
def start(message):
    if message.chat.id == 502102779:
        client.send_message(message.chat.id, 'Введи id,количество месяцев')
        client.register_next_step_handler(message, adminpanel_start)
    else:
        client.send_message(message.chat.id, 'Ой, это команда только для создателя. Как вы вообще о ней узнали?')




##Функция изменения баланса
def change_balance(message, call):
    if message.text.count(',') == 1:
        value = message.text.split(",")[0]
        category = message.text.split(",")[1]
        if is_number(value) == True and int(value) > 0 and int(value) < 2147483647 :
            if isinstance(category, str) == True:
                if category[0] == ' ':
                    category = category[1:]
                if call.data == 'Add':
                    balanceController.change_balance(message.from_user.id, int(value))
                    currentbalance = str(balanceController.current_balance(message.from_user.id))
                    balanceController.new_cell(message.from_user.id, True, category, int(value))
                    balanceController.add_to_all_earnings(message.from_user.id, int(value))
                    client.send_message(message.chat.id, '➕Доход в размере ' + str(value) + ' успешно записан')
                    client.send_message(message.chat.id, 'Твой баланс: ' + currentbalance)
                elif call.data == 'Expense':
                    balanceController.change_balance(message.from_user.id, int(value) * -1)
                    currentbalance = str(balanceController.current_balance(message.from_user.id))
                    balanceController.add_to_all_expense(message.from_user.id, int(value))
                    balanceController.new_cell(message.from_user.id, False, category, int(value))
                    client.send_message(message.chat.id, '➖Расход в размере ' + str(value) + ' успешно записан')
                    client.send_message(message.chat.id, 'Твой баланс: ' + currentbalance)
            else:
                client.send_message(message.chat.id, 'Ошибка ввода: категория введена неверно')
        else:
            client.send_message(message.chat.id, 'Ошибка ввода: число не является целым')
    else:
        client.send_message(message.chat.id, 'Ошибка ввода: неправильный формат')
##Функция вывода дохода за месяц
def month_earnings(id, month, month_text):
    output_month_earnings = balanceController.output_month_earnings(id, str(month))
    if len(output_month_earnings) == 0:
        client.send_message(id, "У вас нет доходов за этот месяц")
    else:
        month_earnings = []
        for i in output_month_earnings:
            category = "\nКатегория: " + str(i[0])
            value = "\nСумма: " + str(i[1])
            date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                '%d.%m | %H:%M | %a') + '\n'
            all = category + value + date
            month_earnings.append(all)

        category_array = balanceController.output_all_add_category_month(id, str(month))
        value_array = balanceController.output_sum_earnings_groupby_category_month(id, str(month))
        url = chart.draw_chart(category_array, value_array)
        img = urllib.request.urlopen(url).read()
        month_earning_sum = str(balanceController.output_month_sum_earnings(id, str(month)))

        text = "Все твои доходы за " + month_text + '\nВсего заработано: ' + month_earning_sum + str(month_earnings).replace("[", "").replace("'", "").replace("]", "").replace(",","").replace("\\n", "\n")
        client.send_photo(id, img, text)


##Функция вывода расхода за месяц
def month_expenses(id, month, month_text):
    output_month_expenses = balanceController.output_month_expenses(id, str(month))
    if len(output_month_expenses) == 0:
        client.send_message(id, "У вас нет расходов за этот месяц")
    else:
        month_expenses = []
        for i in output_month_expenses:
            category = "\nКатегория: " + str(i[0])
            value = "\nСумма: " + str(i[1])
            date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                '%d.%m | %H:%M | %a') + '\n'
            all = category + value + date
            month_expenses.append(all)

        category_array = balanceController.output_all_expense_category_month(id, str(month))
        value_array = balanceController.output_sum_expense_groupby_category_month(id, str(month))
        url = chart.draw_chart(category_array, value_array)
        month_expense_sum = str(balanceController.output_month_sum_expense(id, str(month)))
        img = urllib.request.urlopen(url).read()
        text = '\nВсего потрачено: ' + month_expense_sum + "\nВсе твои расходы за " + month_text +  str(month_expenses).replace("[", "").replace("'", "").replace("]", "").replace(",","").replace("\\n", "\n")
        client.send_photo(id, img, text)

def category_earnings(message):
    category = message.text
    output_category_earnings = balanceController.output_category_earnings(message.chat.id, category)
    if len(output_category_earnings) == 0:
        client.send_message(message.chat.id, "У вас нет доходов в этой категории")
    else:
        all_earnings = balanceController.current_all_earnings(message.chat.id)
        sum_category = balanceController.output_sum_category(message.chat.id, category)
        category_earnings = []
        value_array = []
        for i in output_category_earnings:
            value = "\nСумма: " + str(i[1])
            value_array.append(str(i[1]))
            date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                '%d.%m | %H:%M | %a') + '\n'
            all = value + date
            category_earnings.append(all)

        text = "Всего заработано:  " + str(sum_category) + "\nВсе твои доходы в категории " + category + ':\n' + str(category_earnings).replace("[", "").replace("'", "").replace("]",                                                                                                         "").replace(
            ",", "").replace("\\n", "\n")


        url = chart.draw_chart_for_category(sum_category, all_earnings)
        img = urllib.request.urlopen(url).read()
        client.send_photo(message.chat.id, img, text)




def category_expense(message):
    category = message.text
    output_category_expense = balanceController.output_category_expense(message.chat.id, category)
    if len(output_category_expense) == 0:
        client.send_message(message.chat.id, "У вас нет расходов в этой категории")
    else:
        all_expense = balanceController.current_all_expense(message.chat.id)
        sum_category = balanceController.output_sum_category_expense(message.chat.id, category)
        category_expense = []
        value_array = []
        for i in output_category_expense:
            value = "\nСумма: " + str(i[1])
            value_array.append(str(i[1]))
            date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                '%d.%m | %H:%M | %a') + '\n'
            all = value + date
            category_expense.append(all)
        text = '\nВсего потрачено: ' + str(sum_category) + "\nВсе твои доходы в категории " + category + ':' + str(category_expense).replace("[", "").replace("'", "").replace("]",
                                                                                                                   "").replace(
            ",", "").replace("\\n", "\n")


        url = chart.draw_chart_for_category(sum_category, all_expense)
        img = urllib.request.urlopen(url).read()
        client.send_photo(message.chat.id, img, text)


def is_number(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def check_for_subsribe(tg_id):
    now = datetime.now()
    subsribetime = datetime.strptime(balanceController.output_subscribe_time(tg_id), "%Y-%m-%d %H:%M:%S")
    if ( now <= subsribetime):
        return True
    elif ( now > subsribetime):
        return False

def adminpanel_start(message):
    id = message.text.split(",")[0]
    month = message.text.split(",")[1]
    if len(balanceController.search_user(id)) != 0:
        if is_number(month) == True:
            if balanceController.output_joindate(id) == balanceController.output_subscribe_time(id):
                startdate = datetime.now()
            else:
                startdate = datetime.strptime(balanceController.output_subscribe_time(id), "%Y-%m-%d %H:%M:%S")
            balanceController.change_subscribe_time(id, startdate, month)
        else:
            client.send_message(message.chat.id, 'Ты неправильно ввёл месяц')
    else:
        client.send_message(message.chat.id, 'Такого пользователя не существует')

client.polling(none_stop = True, interval= 0)
