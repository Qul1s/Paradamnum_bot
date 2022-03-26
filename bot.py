import telebot
import configure
from telebot import types
import balanceController
import datetime
from datetime import datetime
import chart
import urllib.request

#Токен
client = telebot.TeleBot(configure.config['token'])

state_of_command = False
@client.message_handler(commands = ['operation'])
def get_user_info(message):
    global state_of_command
    state_of_command = True
    markup_inline = types.InlineKeyboardMarkup()
    if (balanceController.current_language(message.from_user.id)=='RUS'):
        item_add = types.InlineKeyboardButton(text = 'Доход', callback_data = 'Add')
        item_expense = types.InlineKeyboardButton(text='Расход', callback_data='Expense')
        markup_inline.add(item_add, item_expense)
        client.send_message(message.chat.id, 'Выбери действие, будущий олигарх', reply_markup= markup_inline)
    elif(balanceController.current_language(message.from_user.id)=='ENG'):
        item_add = types.InlineKeyboardButton(text='Earning', callback_data='Add')
        item_expense = types.InlineKeyboardButton(text='Expense', callback_data='Expense')
        markup_inline.add(item_add, item_expense)
        client.send_message(message.chat.id, 'Choose an action, future oligarch', reply_markup=markup_inline)

@client.callback_query_handler(func=lambda call:True)
def answer(call):
    global state_of_command
    ##Запись
    if call.data == 'Add':
        if state_of_command == True:
            if (balanceController.current_language(call.message.chat.id) == 'RUS'):
                msg = client.send_message(call.message.chat.id, 'Сколько же ты заработал, мой милый друг?\nФормат: Сумма, Категория')
            elif (balanceController.current_language(call.message.chat.id) == 'ENG'):
                msg = client.send_message(call.message.chat.id, 'How much did you earn, my dear friend?\nFormat: Amount, Category')
            client.register_next_step_handler(msg, change_balance, call)
            state_of_command = False
        else:
            if (balanceController.current_language(call.message.chat.id) == 'RUS'):
                client.send_message(call.message.chat.id, "Вы уже выбирали это")
            elif (balanceController.current_language(call.message.chat.id) == 'ENG'):
                client.send_message(call.message.chat.id, "You've already chosen this")
    elif call.data == 'Expense':
        if state_of_command == True:
            if (balanceController.current_language(call.message.chat.id) == 'RUS'):
                msg = client.send_message(call.message.chat.id, 'Какая сумма была потрачена?\nФормат: Сумма, Категория')
            elif (balanceController.current_language(call.message.chat.id) == 'ENG'):
                msg = client.send_message(call.message.chat.id, 'How much was spent?\nFormat: Amount, Category')
            client.register_next_step_handler(msg, change_balance, call)
            state_of_command = False
        else:
            if (balanceController.current_language(call.message.chat.id) == 'RUS'):
                client.send_message(call.message.chat.id, "Вы уже выбирали это")
            elif (balanceController.current_language(call.message.chat.id) == 'ENG'):
                client.send_message(call.message.chat.id, "You've already chosen this")
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


    elif call.data == 'FAQ':
        photo = open('FAQ.png', 'rb')
        client.send_photo(call.message.chat.id, photo)
    else:
        client.send_message(call.message.chat.id, 'Где-то случилась ошибка')


##Показаль баланс
@client.message_handler(commands = ['balance'])
def get_balance(message):
    currentbalance = str(balanceController.current_balance(message.from_user.id))
    if (balanceController.current_language(message.from_user.id) == 'RUS'):
        client.send_message(message.chat.id, 'Твой баланс: ' + currentbalance)
    elif (balanceController.current_language(message.from_user.id) == 'ENG'):
        client.send_message(message.chat.id, 'Your balance: ' + currentbalance)

##Вывести все категории дохода
@client.message_handler(commands = ['mycategoryearnings'])
def output_all_add_category(message):
    output_all_category_earnings = str(balanceController.output_all_add_category(message.chat.id))
    output = str(output_all_category_earnings).replace("[","").replace("'", "").replace("]","").replace(",", "").replace("(", "").replace(") ", ", ").replace(")", " ")
    if (balanceController.current_language(message.chat.id) == 'RUS'):
        client.send_message(message.chat.id, 'Твои категории дохода:\n' + output)
    elif (balanceController.current_language(message.chat.id) == 'ENG'):
        client.send_message(message.chat.id, 'Your earnings categories: ' + output)
##Вывести все категории расходов
@client.message_handler(commands = ['mycategoryexpense'])
def output_all_expense_category(message):
    output_all_category_expense = str(balanceController.output_all_expense_category(message.from_user.id))
    output = str(output_all_category_expense).replace("[", "").replace("'", "").replace("]", "").replace(",", "").replace("(","").replace(") ", ", ").replace(")", " ")
    if (balanceController.current_language(message.chat.id) == 'RUS'):
        client.send_message(message.chat.id, 'Твои категории расхода:\n' + output)
    elif(balanceController.current_language(message.chat.id) == 'ENG'):
        client.send_message(message.chat.id, 'Your expenses categories:\n' + output)
##Вывести все доходы
@client.message_handler(commands = ['allearnings'])
def all_earnings(message):
    all_earnings = balanceController.output_all_earnings(message.from_user.id)
    if len(all_earnings) == 0:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'Вы еще не вносили ваш доход\nСделать это можно с помощью команды /operation')
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, 'You have not yet deposited your earnings\nThis can be done by using the command /operation')
    else:
        earnings = []
        for i in all_earnings:
            if (balanceController.current_language(message.chat.id) == 'RUS'):
                category = "\n\nКатегория: " + str(i[0])
                value = "\nСумма: " + str(i[1])
                date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m | %H:%M | %a')
            elif (balanceController.current_language(message.chat.id) == 'ENG'):
                category = "\n\nCategory: " + str(i[0])
                value = "\nAmount: " + str(i[1])
                date = "\nDate and time: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m | %H:%M | %a')
            all = category + value + date
            earnings.append(all)

        category_array = balanceController.output_all_add_category(message.chat.id)
        value_array = balanceController.output_sum_earnings_groupby_category(message.chat.id)
        url = chart.draw_chart(category_array, value_array)
        img = urllib.request.urlopen(url).read()
        all_earnings_sum = str(balanceController.current_all_earnings(message.chat.id))
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            text = "\nВсе твои доходы: " +  str(earnings).replace("[","").replace("'", "").replace("]","").replace(",", "").replace("\\n", "\n") + '\nВсего заработано: ' + all_earnings_sum
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            text = "\nAll your earnings: " + str(earnings).replace("[", "").replace("'", "").replace("]", "").replace(",",
                                                                                                                    "").replace(
                "\\n", "\n") + '\nTotal earned: ' + all_earnings_sum
        client.send_message(message.chat.id, text)
        client.send_photo(message.chat.id, img)

##Вывести все расходы
@client.message_handler(commands = ['allexpenses'])
def all_expense(message):
    all_expense = balanceController.output_all_expense(message.from_user.id)
    if len(all_expense) == 0:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'Вы еще не вносили ваши расходы\nСделать это можно с помощью команды /operation')
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id,
                                'You have not listed your expenses yet\nThis can be done by using the command')
    else:
        expense = []
        for i in all_expense:
            if (balanceController.current_language(message.chat.id) == 'RUS'):
                category = "\n\nКатегория: " + str(i[0])
                value = "\nСумма: " + str(i[1])
                date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m | %H:%M | %a')
            elif (balanceController.current_language(message.chat.id) == 'ENG'):
                category = "\n\nCategory: " + str(i[0])
                value = "\nAmount: " + str(i[1])
                date = "\nDate and time: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m | %H:%M | %a')
            all = category + value + date
            expense.append(all)

        category_array = balanceController.output_all_expense_category(message.chat.id)
        value_array = balanceController.output_sum_expense_groupby_category(message.chat.id)
        all_expense_sum = str(balanceController.current_all_expense(message.chat.id))
        url = chart.draw_chart(category_array, value_array)
        img = urllib.request.urlopen(url).read()
        text = "\nВсе твои расходы:"+  str(expense).replace("[","").replace("'", "").replace("]","").replace(",", "").replace("\\n", "\n") + '\nВсего потрачено: ' + all_expense_sum
        client.send_message(message.chat.id, text)
        client.send_photo(message.chat.id, img)

##Вывести все доходы за определённый месяц
@client.message_handler(commands = ['earningsmonth'])
def earnings_month(message):
    if check_for_subsribe(message.chat.id) == True:
        markup_inline = types.InlineKeyboardMarkup()
        if (balanceController.current_language(message.chat.id) == 'RUS'):
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
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            item_January = types.InlineKeyboardButton(text='January', callback_data='January')
            item_February = types.InlineKeyboardButton(text='February', callback_data='February')
            item_March = types.InlineKeyboardButton(text='March', callback_data='March')
            item_April = types.InlineKeyboardButton(text='April', callback_data='April')
            item_May = types.InlineKeyboardButton(text='May', callback_data='May')
            item_June = types.InlineKeyboardButton(text='June', callback_data='June')
            item_July = types.InlineKeyboardButton(text='July', callback_data='July')
            item_August = types.InlineKeyboardButton(text='August', callback_data='August')
            item_September = types.InlineKeyboardButton(text='September', callback_data='September')
            item_October = types.InlineKeyboardButton(text='October', callback_data='October')
            item_November = types.InlineKeyboardButton(text='November', callback_data='November')
            item_December = types.InlineKeyboardButton(text='December', callback_data='December')
        markup_inline.add(item_January, item_February, item_March, item_April, item_May, item_June, item_July, item_August, item_September, item_October, item_November, item_December)
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'Выберите месяц, мой господин', reply_markup=markup_inline)
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, 'Choose a month, my lord', reply_markup=markup_inline)
    else:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'У вас нет доступа к этой команде\nКупить подписку можно командой\n/subscription')
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, 'You do not have access to this command\nYou can buy a subscription with the command\n/subscription')
##Вывести все расходы за определенный месяц
@client.message_handler(commands = ['expensesmonth'])
def expenses_month(message):
    if check_for_subsribe(message.chat.id) == True:
        markup_inline = types.InlineKeyboardMarkup()
        if (balanceController.current_language(message.chat.id) == 'RUS'):
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
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            item_January1 = types.InlineKeyboardButton(text='January', callback_data='January_expense')
            item_February = types.InlineKeyboardButton(text='February', callback_data='February_expense')
            item_March = types.InlineKeyboardButton(text='March', callback_data='March_expense')
            item_April = types.InlineKeyboardButton(text='April', callback_data='April_expense')
            item_May = types.InlineKeyboardButton(text='May', callback_data='May_expense')
            item_June = types.InlineKeyboardButton(text='June', callback_data='June_expense')
            item_July = types.InlineKeyboardButton(text='July', callback_data='July_expense')
            item_August = types.InlineKeyboardButton(text='August', callback_data='August_expense')
            item_September = types.InlineKeyboardButton(text='September', callback_data='September_expense')
            item_October = types.InlineKeyboardButton(text='October', callback_data='October_expense')
            item_November = types.InlineKeyboardButton(text='November', callback_data='November_expense')
            item_December = types.InlineKeyboardButton(text='December', callback_data='December_expense')
        markup_inline.add(item_January1, item_February, item_March, item_April, item_May, item_June, item_July, item_August, item_September, item_October, item_November, item_December)

        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'Выберите месяц, мой господин', reply_markup=markup_inline)
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, 'Choose a month, my lord', reply_markup=markup_inline)
    else:
            if (balanceController.current_language(message.chat.id) == 'RUS'):
                client.send_message(message.chat.id,
                                    'У вас нет доступа к этой команде\nКупить подписку можно командой\n/subscription')
            elif (balanceController.current_language(message.chat.id) == 'ENG'):
                client.send_message(message.chat.id,
                                    'You do not have access to this command\nYou can buy a subscription with the command\n/subscription')
#Вывод доходов в заданной категории
@client.message_handler(commands = ['earningscategory'])
def categoryearnings(message):
    if check_for_subsribe(message.chat.id) == True:
        output_all_category = str(balanceController.output_all_add_category(message.from_user.id))
        output = str(output_all_category).replace("[", "").replace("'", "").replace("]", "").replace(",", "").replace("(",
                                                                                                                      "").replace(
            ") ", ", ").replace(")", " ")
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'Введите категорию\nТвои категории дохода:\n' + output)
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, 'Enter a category\nYour earnings categories:\n' + output)
        client.register_next_step_handler(message, category_earnings)
    else:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id,
                                'У вас нет доступа к этой команде\nКупить подписку можно командой\n/subscription')
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id,
                                'You do not have access to this command\nYou can buy a subscription with the command\n/subscription')
#Вывод расходов в заданной категории
@client.message_handler(commands = ['expensecategory'])
def categoryexpense(message):
    if check_for_subsribe(message.chat.id) == True:
        output_all_category = str(balanceController.output_all_expense_category(message.from_user.id))
        output = str(output_all_category).replace("[", "").replace("'", "").replace("]", "").replace(",", "").replace("(",
                                                                                                                      "").replace(
            ") ", ", ").replace(")", " ")
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'Введите категорию\nТвои категории дохода:\n' + output)
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, 'Enter a category\nYour expenses categories:\n' + output)
        client.register_next_step_handler(message, category_expense)
    else:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id,
                                'У вас нет доступа к этой команде\nКупить подписку можно командой\n/subscription')
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id,
                                'You do not have access to this command\nYou can buy a subscription with the command\n/subscription')

##Старт
@client.message_handler(commands = ['start'])
def start(message):
        balanceController.new_user(message.from_user.id)
        photo = open('paradamnumprew.png', 'rb')
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            text = 'Привет, я бот, который поможет тебе контролировать твои денежные ресурсы!😎 \nТвой ID: ' + str(message.from_user.id) + '\nУзнать возможности бота можно по кнопке ниже'
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            text = 'Hi, I am a bot to help you control your money resources!😎\nYour ID: ' + str(
                message.from_user.id) + '\nTo learn more about the bots capabilities, click the button below'
        markup_inline = types.InlineKeyboardMarkup()
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            faq = types.InlineKeyboardButton(text='Узнать возможности', callback_data='FAQ')
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            faq = types.InlineKeyboardButton(text='Find out whats possible', callback_data='FAQ')
        markup_inline.add(faq)
        client.send_photo(message.chat.id, photo, text, reply_markup=markup_inline)
##Разработчики
@client.message_handler(commands = ['developers'])
def start(message):
    if (balanceController.current_language(message.chat.id) == 'RUS'):
        client.send_message(message.chat.id, 'Бот был создан: @retiunskykh')
    elif (balanceController.current_language(message.chat.id) == 'ENG'):
        client.send_message(message.chat.id, 'The bot was created by @retiunskykh')
##Подписка
@client.message_handler(commands = ['subscription'])
def start(message):
    subsribetime = datetime.strptime(balanceController.output_subscribe_time(message.chat.id), "%Y-%m-%d %H:%M:%S")
    if check_for_subsribe(message.chat.id) == True:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'У вас есть подписка, которая действует до: ' + str(subsribetime.strftime('%Y-%m-%d')))
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id,
                                'You have a subscription that is valid until: ' + str(subsribetime.strftime('%Y-%m-%d')))
    elif check_for_subsribe(message.chat.id) == False:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'У вас нет подписки\nЧтобы купить подписку выберите тариф снизу\nДо 6 месяцев - 1.99$/месяц\n6 месяцев - 9.99$\n1 год - 17.99$\nПо поводу покупки писать: @retiunskykh\nИли оплатите заданную сумму на карту: 4441 1144 1244 6062\nВ комментариях указать свой ID: '+ str(message.chat.id))
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id,
                                'You do not have a subscription\nTo buy a subscription, select a rate from below\nUp to 6 months - $1.99/month\n6 months - $9.99\n1 year - $17.99\nTo write about the purchase: @retiunskykh\nOr pay a set amount to the card: 4441 1144 1244 6062\nEnter your ID in the comments: ' + str(
                                    message.chat.id))
##АдминПанель
@client.message_handler(commands = ['adminpanel'])
def start(message):
    if message.chat.id == 502102779:
        client.send_message(message.chat.id, 'Введи id,количество месяцев')
        client.register_next_step_handler(message, adminpanel_start)
    else:
        client.send_message(message.chat.id, 'Ой, это команда только для создателя. Как вы вообще о ней узнали?')
#Удалить запись
@client.message_handler(commands = ['deleterecord'])
def start(message):
    if (balanceController.current_language(message.chat.id) == 'RUS'):
        client.send_message(message.chat.id, 'Введи сумму, категорию, дату\nНапример: 200, Еда, 2022-02-12 10:00')
    elif (balanceController.current_language(message.chat.id) == 'ENG'):
        client.send_message(message.chat.id, 'Enter amount, category, date\nFor example: 200, Food, 2022-02-12 10:00')
    client.register_next_step_handler(message, delete_record)


@client.message_handler(commands = ['FAQ'])
def start(message):
    photo = open('FAQ.png', 'rb')
    client.send_photo(message.chat.id, photo)
#Ввод случайного текста
@client.message_handler(content_types='text')
def start(message):
    if (balanceController.current_language(message.chat.id) == 'RUS'):
        client.send_message(message.chat.id, 'Cначала введите команду😄')
    elif (balanceController.current_language(message.chat.id) == 'RUS'):
        client.send_message(message.chat.id, 'First, enter the command😄')
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
                    if (balanceController.current_language(message.chat.id) == 'RUS'):
                        client.send_message(message.chat.id, '➕Доход в размере ' + str(value) + ' успешно записан')
                        client.send_message(message.chat.id, 'Твой баланс: ' + currentbalance)
                    elif (balanceController.current_language(message.chat.id) == 'ENG'):
                        client.send_message(message.chat.id, '➕Earnings in the amount of ' + str(value) + ' successfully recorded')
                        client.send_message(message.chat.id, 'Your balance: ' + currentbalance)
                elif call.data == 'Expense':
                    balanceController.change_balance(message.from_user.id, int(value) * -1)
                    currentbalance = str(balanceController.current_balance(message.from_user.id))
                    balanceController.add_to_all_expense(message.from_user.id, int(value))
                    balanceController.new_cell(message.from_user.id, False, category, int(value))
                    if (balanceController.current_language(message.chat.id) == 'RUS'):
                        client.send_message(message.chat.id, '➖Расход в размере ' + str(value) + ' успешно записан')
                        client.send_message(message.chat.id, 'Твой баланс: ' + currentbalance)
                    elif (balanceController.current_language(message.chat.id) == 'ENG'):
                        client.send_message(message.chat.id, '➖Expenses in the amount of ' + str(value) + ' successfully recorded')
                        client.send_message(message.chat.id, 'Your balance: ' + currentbalance)
            else:
                if (balanceController.current_language(message.chat.id) == 'RUS'):
                    client.send_message(message.chat.id, 'Ошибка ввода: категория введена неверно')
                elif (balanceController.current_language(message.chat.id) == 'ENG'):
                    client.send_message(message.chat.id, 'Input error: category entered incorrectly')
        else:
            if (balanceController.current_language(message.chat.id) == 'RUS'):
                client.send_message(message.chat.id, 'Ошибка ввода: число не является целым')
            elif (balanceController.current_language(message.chat.id) == 'ENG'):
                client.send_message(message.chat.id, 'Input error: the number is not an integer')
    else:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'Ошибка ввода: неправильный формат')
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, 'Input error: Incorrect format')
##Функция вывода дохода за месяц
def month_earnings(id, month, month_text):
    output_month_earnings = balanceController.output_month_earnings(id, str(month))
    if len(output_month_earnings) == 0:
        if (balanceController.current_language(id) == 'RUS'):
            client.send_message(id, "У вас нет доходов за этот месяц")
        elif (balanceController.current_language(id) == 'ENG'):
            client.send_message(id, 'You have no earnings for this month')

    else:
        month_earnings = []
        for i in output_month_earnings:
            if (balanceController.current_language(id) == 'RUS'):
                category = "\nКатегория: " + str(i[0])
                value = "\nСумма: " + str(i[1])
                date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                    '%d.%m | %H:%M | %a') + '\n'
            elif (balanceController.current_language(id) == 'ENG'):
                category = "\nCategory: " + str(i[0])
                value = "\nAmount: " + str(i[1])
                date = "\nDate and time: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                    '%d.%m | %H:%M | %a') + '\n'

            all = category + value + date
            month_earnings.append(all)

        category_array = balanceController.output_all_add_category_month(id, str(month))
        value_array = balanceController.output_sum_earnings_groupby_category_month(id, str(month))
        url = chart.draw_chart(category_array, value_array)
        img = urllib.request.urlopen(url).read()
        month_earning_sum = str(balanceController.output_month_sum_earnings(id, str(month)))
        if (balanceController.current_language(id) == 'RUS'):
            text = "Все твои доходы за " + month_text + str(month_earnings).replace("[", "").replace("'", "").replace("]", "").replace(",","").replace("\\n", "\n") + '\nВсего заработано: ' + month_earning_sum
        elif (balanceController.current_language(id) == 'ENG'):
            text = "All your income for " + month_text + str(month_earnings).replace("[", "").replace("'", "").replace("]", "").replace(",","").replace("\\n", "\n") + '\nTotal earned: ' + month_earning_sum
        client.send_message(id, text)
        client.send_photo(id, img)



##Функция вывода расхода за месяц
def month_expenses(id, month, month_text):
    output_month_expenses = balanceController.output_month_expenses(id, str(month))
    if len(output_month_expenses) == 0:
        if (balanceController.current_language(id) == 'RUS'):
            client.send_message(id, "У вас нет расходов за этот месяц")
        elif (balanceController.current_language(id) == 'ENG'):
            client.send_message(id, "You have no expenses for this month")
    else:
        month_expenses = []
        for i in output_month_expenses:
            if (balanceController.current_language(id) == 'RUS'):
                category = "\nКатегория: " + str(i[0])
                value = "\nСумма: " + str(i[1])
                date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                    '%d.%m | %H:%M | %a') + '\n'
            elif (balanceController.current_language(id) == 'ENG'):
                category = "\nCategory: " + str(i[0])
                value = "\nAmount: " + str(i[1])
                date = "\nDate and time: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                    '%d.%m | %H:%M | %a') + '\n'

            all = category + value + date
            month_expenses.append(all)

        category_array = balanceController.output_all_expense_category_month(id, str(month))
        value_array = balanceController.output_sum_expense_groupby_category_month(id, str(month))
        url = chart.draw_chart(category_array, value_array)
        month_expense_sum = str(balanceController.output_month_sum_expense(id, str(month)))
        img = urllib.request.urlopen(url).read()
        if (balanceController.current_language(id) == 'RUS'):
            text = "\nВсе твои расходы за " + month_text +  str(month_expenses).replace("[", "").replace("'", "").replace("]", "").replace(",","").replace("\\n", "\n")+'\nВсего потрачено: ' + month_expense_sum
        elif (balanceController.current_language(id) == 'ENG'):
            text = "\nAll your expenses for " + month_text +  str(month_expenses).replace("[", "").replace("'", "").replace("]", "").replace(",","").replace("\\n", "\n")+'\nTotal spent: ' + month_expense_sum
        client.send_message(id, text)
        client.send_photo(id, img)

##Функция вывода дохода по категории
def category_earnings(message):
    category = message.text
    output_category_earnings = balanceController.output_category_earnings(message.chat.id, category)
    if len(output_category_earnings) == 0:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, "У вас нет доходов в этой категории")
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, "You have no earnings in this category")

    else:
        all_earnings = balanceController.current_all_earnings(message.chat.id)
        sum_category = balanceController.output_sum_category(message.chat.id, category)
        category_earnings = []
        value_array = []
        for i in output_category_earnings:
            if (balanceController.current_language(message.chat.id) == 'RUS'):
                value = "\nСумма: " + str(i[1])
                value_array.append(str(i[1]))
                date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                    '%d.%m | %H:%M | %a') + '\n'
            elif (balanceController.current_language(message.chat.id) == 'ENG'):
                value = "\nCategory: " + str(i[1])
                value_array.append(str(i[1]))
                date = "\nDate and time: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                    '%d.%m | %H:%M | %a') + '\n'

            all = value + date
            category_earnings.append(all)

        if (balanceController.current_language(message.chat.id) == 'RUS'):
            text = "\nВсе твои доходы в категории " + category + ':\n' + str(category_earnings).replace("[",
                                                                                                        "").replace("'",
                                                                                                                    "").replace(
                "]", "").replace(
                ",", "").replace("\\n", "\n") + "Всего заработано:  " + str(sum_category)
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            text = "\nAll your earnings in the category " + category + ':\n' + str(category_earnings).replace("[",
                                                                                                        "").replace("'",
                                                                                                                    "").replace(
                "]", "").replace(
                ",", "").replace("\\n", "\n") + "Total earned:  " + str(sum_category)

        url = chart.draw_chart_for_category(sum_category, all_earnings)
        img = urllib.request.urlopen(url).read()
        client.send_message(message.chat.id, text)
        client.send_photo(message.chat.id, img)
##Функция вывода расхода по категории
def category_expense(message):
    category = message.text
    output_category_expense = balanceController.output_category_expense(message.chat.id, category)
    if len(output_category_expense) == 0:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, "У вас нет расходов в этой категории")
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, "You have no expenses in this category")

    else:
        all_expense = balanceController.current_all_expense(message.chat.id)
        sum_category = balanceController.output_sum_category_expense(message.chat.id, category)
        category_expense = []
        value_array = []
        for i in output_category_expense:
            if (balanceController.current_language(message.chat.id) == 'RUS'):
                value = "\nСумма: " + str(i[1])
                value_array.append(str(i[1]))
                date = "\nДата и время: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                    '%d.%m | %H:%M | %a') + '\n'
            elif (balanceController.current_language(message.chat.id) == 'ENG'):
                value = "\nCategory: " + str(i[1])
                value_array.append(str(i[1]))
                date = "\nDate and time: " + datetime.strptime(str(i[2]), '%Y-%m-%d %H:%M:%S').strftime(
                    '%d.%m | %H:%M | %a') + '\n'
            all = value + date
            category_expense.append(all)

        if (balanceController.current_language(message.chat.id) == 'RUS'):
            text =  "\nВсе твои доходы в категории " + category + ':' + str(category_expense).replace("[", "").replace("'", "").replace("]",
                                                                                                                   "").replace(
            ",", "").replace("\\n", "\n") + '\nВсего потрачено: ' + str(sum_category)
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            text = "\nAll your earnings in the category " + category + ':' + str(category_expense).replace("[", "").replace(
                "'", "").replace("]",
                                 "").replace(
                ",", "").replace("\\n", "\n") + '\nTotal spent: ' + str(sum_category)

        url = chart.draw_chart_for_category(sum_category, all_expense)
        img = urllib.request.urlopen(url).read()
        client.send_message(message.chat.id, text)
        client.send_photo(message.chat.id, img)

#Функция проверки на число
def is_number(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
#Функция проверки на дату
def is_date(str):
    try:
        datetime.strptime(str, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False
#Проверка на подписку
def check_for_subsribe(tg_id):
    now = datetime.now()
    subsribetime = datetime.strptime(balanceController.output_subscribe_time(tg_id), "%Y-%m-%d %H:%M:%S")
    if ( now <= subsribetime):
        return True
    elif ( now > subsribetime):
        return False
#АдминПанель
def adminpanel_start(message):
    if message.text.count(',') == 1:
        id = message.text.split(",")[0]
        month = message.text.split(",")[1]
        if balanceController.search_user(id) == 1:
            if is_number(month) == True:
                if balanceController.output_joindate(id) == balanceController.output_subscribe_time(id):
                    startdate = datetime.now()
                else:
                    startdate = datetime.strptime(balanceController.output_subscribe_time(id), "%Y-%m-%d %H:%M:%S")
                balanceController.change_subscribe_time(id, startdate, month)
                client.send_message(message.chat.id, 'Успешно')
            else:
                client.send_message(message.chat.id, 'Ты неправильно ввёл месяц')
        else:
            client.send_message(message.chat.id, 'Такого пользователя не существует')
    else:
        client.send_message(message.chat.id, 'Неправильный формат')
#Удалить запись(метод)
def delete_record(message):
    if message.text.count(',') == 2:
        value = message.text.split(",")[0]
        category = message.text.split(",")[1]
        date = message.text.split(",")[2]
        if date[0] == ' ':
            date = date[1:]
        if is_number(value) == True and int(value) > 0 and int(value) < 2147483647 :
            if isinstance(category, str) == True:
                if is_date(date) == True:
                    if category[0] == ' ':
                        category = category[1:]
                    if balanceController.check_for_record(message.chat.id, value, category, date) == 1:
                        if int(balanceController.check_operation(message.chat.id, value, category, date)) == 1:
                            balanceController.change_balance(message.from_user.id, int(value)*-1)
                            balanceController.add_to_all_earnings(message.from_user.id, int(value)*-1)
                        elif int(balanceController.check_operation(message.chat.id, value, category, date)) == 0:
                            balanceController.change_balance(message.from_user.id, int(value))
                            balanceController.add_to_all_expense(message.from_user.id, int(value) * -1)
                        balanceController.delete_record(message.chat.id, value, category, date)
                        if (balanceController.current_language(message.chat.id) == 'RUS'):
                            client.send_message(message.chat.id, 'Запись успешно удалена')
                        elif (balanceController.current_language(message.chat.id) == 'ENG'):
                            client.send_message(message.chat.id, "Entry successfully deleted")
                    else:
                        if (balanceController.current_language(message.chat.id) == 'RUS'):
                            client.send_message(message.chat.id, 'Запись не найдена')
                        elif (balanceController.current_language(message.chat.id) == 'ENG'):
                            client.send_message(message.chat.id, "No entry found")
                else:
                    if (balanceController.current_language(message.chat.id) == 'RUS'):
                        client.send_message(message.chat.id, 'Неправильно введена дата')
                    elif (balanceController.current_language(message.chat.id) == 'ENG'):
                        client.send_message(message.chat.id, "Incorrect date entered")
            else:
                if (balanceController.current_language(message.chat.id) == 'RUS'):
                    client.send_message(message.chat.id, 'Ошибка ввода: категория введена неверно')
                elif (balanceController.current_language(message.chat.id) == 'ENG'):
                    client.send_message(message.chat.id, "Input error: category entered incorrectly")
        else:
            if (balanceController.current_language(message.chat.id) == 'RUS'):
                client.send_message(message.chat.id, 'Ошибка ввода: число не является целым')
            elif (balanceController.current_language(message.chat.id) == 'ENG'):
                client.send_message(message.chat.id, "Input error: the number is not an integer")
    else:
        if (balanceController.current_language(message.chat.id) == 'RUS'):
            client.send_message(message.chat.id, 'Ошибка ввода: неправильный формат')
        elif (balanceController.current_language(message.chat.id) == 'ENG'):
            client.send_message(message.chat.id, "Input error: Incorrect format")

#Важная фигня, всегда в конце
client.polling(none_stop = True, interval= 0)