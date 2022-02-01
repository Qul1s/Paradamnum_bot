import datetime
import sqlite3
from datetime import datetime
from dateutil.relativedelta import *

def new_user(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (tg_id,))
    conn.commit()
    conn.close()

def change_balance(tg_id, value):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (value,tg_id,))
    conn.commit()
    conn.close()


def current_balance(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    currentbalance = cursor.execute("SELECT balance FROM users WHERE user_id =?", (tg_id,))
    conn.commit()
    return currentbalance.fetchone()[0]

def current_all_earnings(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    current_all_earnings = cursor.execute("SELECT all_earnings FROM users WHERE user_id =?", (tg_id,))
    conn.commit()
    return current_all_earnings.fetchone()[0]

def current_all_expense(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    current_all_expense = cursor.execute("SELECT all_expense FROM users WHERE user_id =?", (tg_id,))
    conn.commit()
    return current_all_expense.fetchone()[0]


def new_cell(tg_id, operation, category, value):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO 'records' ('user_id',operation, category, value) VALUES (?, ?, ?, ?)", (tg_id, operation, category, value, ))
    conn.commit()
    conn.close()

def add_to_all_earnings(tg_id, value):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET all_earnings = all_earnings + ? WHERE user_id = ?", (value,tg_id,))
    conn.commit()
    conn.close()

def add_to_all_expense(tg_id, value):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET all_expense = all_expense + ? WHERE user_id = ?", (value,tg_id,))
    conn.commit()
    conn.close()

def output_all_add_category(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    all_category_earnings = cursor.execute("SELECT DISTINCT category FROM records WHERE user_id =? and operation = True", (tg_id,))
    conn.commit()
    all_category_earnings_array = []
    while True:
        row = all_category_earnings.fetchone()
        if row == None:
            break
        else:
            all_category_earnings_array.append(row)
    return all_category_earnings_array


def output_all_expense_category(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    all_category_expense = cursor.execute("SELECT DISTINCT category FROM records WHERE user_id =? and operation = False", (tg_id,))
    conn.commit()
    all_category_expense_array = []
    while True:
        row = all_category_expense.fetchone()
        if row == None:
            break
        else:
            all_category_expense_array.append(row)
    return all_category_expense_array


def output_all_earnings(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    all_earnings = cursor.execute("SELECT category, value, date FROM records WHERE user_id =? and operation = True", (tg_id,))
    conn.commit()
    all_earnings_array = []
    while True:
        row = all_earnings.fetchone()
        if row  == None:
            break
        else:
            all_earnings_array.append(row)
    return all_earnings_array

def output_all_expense(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    all_expense = cursor.execute("SELECT category, value, date FROM records WHERE user_id =? and operation = False", (tg_id,))
    conn.commit()
    all_expense_array = []
    while True:
        row = all_expense.fetchone()
        if row  == None:
            break
        else:
            all_expense_array.append(row)
    return all_expense_array


def output_month_earnings(tg_id, month):
    now = datetime.now()
    if int(now.month) < 6 and int(month) > 6:
        year = int(now.year) - 1
    else:
        year = int(now.year)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    month_earnings = cursor.execute("SELECT category, value, date FROM records WHERE user_id = ? and operation = True and strftime('%m', date) = ? and strftime('%Y', date) = ?", (tg_id, month, str(year),))
    conn.commit()
    all_month_earnings =[]
    while True:
        row = month_earnings.fetchone()
        if row  == None:
            break
        else:
            all_month_earnings.append(row)
    return all_month_earnings

def output_month_expenses(tg_id, month):
    now = datetime.now()
    if int(now.month) < 6 and int(month) > 6:
        year = int(now.year) - 1
    else:
        year = int(now.year)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    month_expenses = cursor.execute("SELECT category, value, date FROM records WHERE user_id = ? and operation = False and strftime('%m', date) =? and strftime('%Y', date) = ?", (tg_id, month, str(year),))
    conn.commit()
    all_month_expenses =[]
    while True:
        row = month_expenses.fetchone()
        if row  == None:
            break
        else:
            all_month_expenses.append(row)
    return all_month_expenses


def output_category_earnings(tg_id, category):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    category_earnings = cursor.execute("SELECT category, value, date FROM records WHERE user_id = ? and operation = True and category = ?", (tg_id, category))
    conn.commit()
    all_category_earnings =[]
    while True:
        row = category_earnings.fetchone()
        if row  == None:
            break
        else:
            all_category_earnings.append(row)
    return all_category_earnings

def output_sum_category(tg_id, category):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    output_sum_category = cursor.execute("SELECT sum(value) FROM records WHERE user_id = ? and operation = True and category = ?",(tg_id, category))
    conn.commit()
    return output_sum_category.fetchone()[0]



def output_category_expense(tg_id, category):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    category_expenses = cursor.execute("SELECT category, value, date FROM records WHERE user_id = ? and operation = False and category = ?", (tg_id, category))
    conn.commit()
    all_category_expenses =[]
    while True:
        row = category_expenses.fetchone()
        if row  == None:
            break
        else:
            all_category_expenses.append(row)
    return all_category_expenses

def output_sum_category_expense(tg_id, category):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    output_sum_category = cursor.execute("SELECT sum(value) FROM records WHERE user_id = ? and operation = False and category = ?",(tg_id, category))
    conn.commit()
    return output_sum_category.fetchone()[0]

def output_sum_expense_groupby_category(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    output_sum_category = cursor.execute("SELECT sum(value) FROM records WHERE user_id = ? and operation = False GROUP BY category", (tg_id,))
    conn.commit()
    output_sum_category_array= []
    while True:
        row = output_sum_category.fetchone()
        if row == None:
            break
        else:
            output_sum_category_array.append(row)
    return output_sum_category_array


def output_sum_earnings_groupby_category(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    output_sum_category = cursor.execute("SELECT sum(value) FROM records WHERE user_id = ? and operation = True GROUP BY category", (tg_id,))
    conn.commit()
    output_sum_category_array= []
    while True:
        row = output_sum_category.fetchone()
        if row == None:
            break
        else:
            output_sum_category_array.append(row)
    return output_sum_category_array


def output_subscribe_time(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    currentbalance = cursor.execute("SELECT subscribe_date FROM users WHERE user_id =?", (tg_id,))
    conn.commit()
    return currentbalance.fetchone()[0]


def output_joindate(tg_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    currentbalance = cursor.execute("SELECT joindate FROM users WHERE user_id =?", (tg_id,))
    conn.commit()
    return currentbalance.fetchone()[0]

def change_subscribe_time(tg_id, startdate, month):
    date = startdate + relativedelta(months=+int(month))
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET subscribe_date = ? WHERE user_id = ?", (date, tg_id,))
    conn.commit()
    conn.close()


def output_all_add_category_month(tg_id, month):
    now = datetime.now()
    if int(now.month) < 6 and int(month) > 6:
        year = int(now.year) - 1
    else:
        year = int(now.year)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    all_category_earnings = cursor.execute("SELECT DISTINCT category FROM records WHERE user_id =? and operation = True and strftime('%m', date) =? and strftime('%Y', date) = ?", (tg_id, month, str(year),))
    conn.commit()
    all_category_earnings_array = []
    while True:
        row = all_category_earnings.fetchone()
        if row == None:
            break
        else:
            all_category_earnings_array.append(row)
    return all_category_earnings_array


def output_all_expense_category_month(tg_id, month):
    now = datetime.now()
    if int(now.month) < 6 and int(month) > 6:
        year = int(now.year) - 1
    else:
        year = int(now.year)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    all_category_expense = cursor.execute("SELECT DISTINCT category FROM records WHERE user_id =? and operation = False and strftime('%m', date) =? and strftime('%Y', date) = ?", (tg_id, month, str(year),))
    conn.commit()
    all_category_expense_array = []
    while True:
        row = all_category_expense.fetchone()
        if row == None:
            break
        else:
            all_category_expense_array.append(row)
    return all_category_expense_array


def output_sum_expense_groupby_category_month(tg_id, month):
    now = datetime.now()
    if int(now.month) < 6 and int(month) > 6:
        year = int(now.year) - 1
    else:
        year = int(now.year)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    output_sum_category = cursor.execute("SELECT sum(value) FROM records WHERE user_id = ? and operation = False and strftime('%m', date) =? and strftime('%Y', date) = ? GROUP BY category", (tg_id, month, str(year),))
    conn.commit()
    output_sum_category_array= []
    while True:
        row = output_sum_category.fetchone()
        if row == None:
            break
        else:
            output_sum_category_array.append(row)
    return output_sum_category_array


def output_sum_earnings_groupby_category_month(tg_id, month):
    now = datetime.now()
    if int(now.month) < 6 and int(month) > 6:
        year = int(now.year) - 1
    else:
        year = int(now.year)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    output_sum_category = cursor.execute("SELECT sum(value) FROM records WHERE user_id = ? and operation = True and strftime('%m', date) =? and strftime('%Y', date) = ? GROUP BY category", (tg_id, month, str(year),))
    output_sum_category_array= []
    while True:
        row = output_sum_category.fetchone()
        if row == None:
            break
        else:
            output_sum_category_array.append(row)
    return output_sum_category_array


