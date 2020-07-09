#!/bin/python3

import urllib.request
import argparse
from create_db import userdb
import telethon
import stringsConstant as sc
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telethon import sync, events
import requests
import json
import time
import re
from telethon import TelegramClient
import webbrowser
import urllib.request
import os
import sqlite3
from flask import Flask
from threading import Thread



db = sqlite3.connect('Account.db', check_same_thread=False)

clientarr = []

def napClientArr():
    global balance
    curw = db.cursor()
    curw.execute("SELECT * FROM Account")
    for item in curw.fetchall():
        session = "anon" + str(item[0])
        print(session, item[3], item[4])
        client = TelegramClient(session, item[3], item[4])
        client.start()
        clientarr.append(client)
    curw.close()
def telegranGetBalance():
    global balance
    curw = db.cursor()
    curw.execute("SELECT * FROM Account")
    balanceTemp = {
        "all": 0,
        "users": [
        ]
    }
    x = 1  # це счетчик
    for client in clientarr:

        dlgs = client.get_dialogs()
        for dlg in dlgs:
            if dlg.title == 'LTC Click Bot':
                tegmo = dlg

        client.send_message('LTC Click Bot', "/balance")
        time.sleep(3)
        msgs = client.get_messages(tegmo, limit=1)

        for mes in msgs:
            str_a = str(mes.message)
            zz = str_a.replace('Available balance: ', '')
            qq = zz.replace(' LTC', '')
            waitin = float(qq)

        balanceTemp["users"].append({"user": str(x), "balance": waitin})
        balanceTemp["all"] = balanceTemp["all"] + waitin
        x = x + 1  # це конкатенация счетчика
    balance = balanceTemp
    print(balance)
    curw.close()
def miner():
    x = 1
    class RunChromeTests():
        def testMethod(self):
            selenium_url = "http://localhost:4444/wd/hub"
            caps = {'browserName': 'chrome'}
            driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps)
            driver.maximize_window()
            driver.get(url_rec)
            time.sleep(waitin + 10)
            driver.close()
            driver.quit()
    counUser = 0
    for w in userdb(db).getUser():
        counUser +=1
    while(True):
        n = 0
        u = 0
        if x > counUser:
            x = x - counUser

        print("Очередь аккаунта № " + str(x))
        client = clientarr[x-1]

        dlgs = client.get_dialogs()
        for dlg in dlgs:
            if dlg.title == 'LTC Click Bot':
                tegmo = dlg
        client.send_message('LTC Click Bot', "🖥 Visit sites")
        time.sleep(30)
        while True:
            time.sleep(6)
            print("Нет заданий уже: " + str(u) + " раз")
            if u == 2:
                print("Переходим на другой аккаунт")
                telegranGetBalance()
                break
            print("Пройдено циклов: " + str(n))
            if n == 10:
                print("Переходим на другой аккаунт")
                telegranGetBalance()
                break
            msgs = client.get_messages(tegmo, limit=1)
            for mes in msgs:
                if re.search(r'\bseconds to get your reward\b', mes.message):
                    print("Найдено reward")
                    str_a = str(mes.message)
                    zz = str_a.replace('You must stay on the site for', '')
                    qq = zz.replace('seconds to get your reward.', '')
                    waitin = int(qq)
                    print ("Ждать придется: ", waitin)
                    client.send_message('LTC Click Bot', "/visit")
                    time.sleep(3)
                    msgs2 = client.get_messages(tegmo, limit=1)
                    for mes2 in msgs2:
                        button_data = mes2.reply_markup.rows[1].buttons[1].data
                        message_id = mes2.id
                        print("Перехожу по ссылке")
                        time.sleep(2)
                        url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                        ch = RunChromeTests()
                        ch.testMethod()
                        time.sleep(6)
                        fp = urllib.request.urlopen(url_rec)
                        mybytes = fp.read()
                        mystr = mybytes.decode("utf8")
                        fp.close()
                        if re.search(r'\bSwitch to reCAPTCHA\b', mystr):
                            from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                            resp = client(GetBotCallbackAnswerRequest(
                                'LTC Click Bot',
                                message_id,
                                data=button_data
                            ))
                            time.sleep(2)
                            print("КАПЧА!")

                        else:
                            time.sleep(waitin)

                            time.sleep(2)
                elif re.search(r'\bSorry\b', mes.message):

                    print("Найдено Sorry")
                    u = u + 1
                    print(u)

                else:
                    messages = client.get_messages('Litecoin_click_bot')
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    f = open("per10.txt")
                    fd = f.read()
                    if fd == url_rec:
                        print("Найдено повторение переменной")
                        msgs2 = client.get_messages(tegmo, limit=1)
                        for mes2 in msgs2:
                            button_data = mes2.reply_markup.rows[1].buttons[1].data
                            message_id = mes2.id
                            from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                            resp = client(GetBotCallbackAnswerRequest(
                                tegmo,
                                message_id,
                                data=button_data
                            ))
                            time.sleep(2)
                    else:
                        waitin = 15
                        data1 = requests.get(url_rec).json
                        print(data1)

                        my_file = open('per10.txt', 'w')
                        my_file.write(url_rec)
                        print("Новая запись в файле сделана")
                        time.sleep(16)
                        n = n + 1

                        if n == 10:
                            break
        time.sleep(1)
        x = x + 1
        if x == counUser:
            break
def server():
    global balance
    app = Flask(__name__)
    @app.route('/')
    def index():
        return 'it is api bro'

    @app.route('/balance')
    def getBalance():
        global balance
        return json.dumps(balance)

    app.run(host="0.0.0.0", port=8080)
def stresMiner():
    try:
        miner()
    except Exception:
        stresMiner()
def maining(args):
    napClientArr()
    telegranGetBalance()
    variable = Thread(target=server)
    variable.start()
    stresMiner()
def addUser(args):
    user = userdb(db)
    user.addUser(
        input("Phone: "),
        input("password: "),
        input("Api_id: "),
        input("Api_hash: "),
        input("Activity: "),
        input("Litecoin: "))
    print("addUser")
def delUser(args):
    print(args)
    user = userdb(db)
    user.delUser(args.id)
    print("delUser")
def listUser(args):
    print(args)
    user = userdb(db)
    for item in user.getUser():
        print("#####################\n")
        print("id: " + str(item[0]))
        print("phone: " + item[1])
        print("Api_id: " + item[2])
        print("Api_hash: " + item[3])
        print("Activity: " + item[4])
        print("Litecoin: " + item[5])
def createClient(args):
    user = userdb(db)
    print(user.getUser())
    for item in user.getUser():
        print("Очередь аккаунта № " + str(item[0]))
        Phone = str(item[1])
        print("Входим в аккаунт: " + Phone)
        password = str(item[2])
        print("password: " + password)
        api_id = str(item[3])
        api_hash = str(item[4])
        session = str("anon" + str(item[0]))
        client = TelegramClient(session, api_id, api_hash)
        try:
            client.start()
            time.sleep(1)
        except telethon.errors.rpcerrorlist.ApiIdInvalidError:
            print("error in "+str(item[0]))
    print("Aккаунты активированы!")

parser = argparse.ArgumentParser(description=sc.description)
def info(args):
    parser.print_usage()
parser.set_defaults(func=info)
subparsers = parser.add_subparsers()

parser_maining = subparsers.add_parser('maining', help=sc.key_maining_desc)
parser_maining.add_argument('-s', '--server-no', action='store_true', help=sc.key_maining_server)
parser_maining.add_argument('-p', '--port', nargs='?', default=8080, help=sc.key_maining_port)
parser_maining.set_defaults(func=maining)


parser_config = subparsers.add_parser('config', help=sc.config)
def info_config(args):
    parser_config.print_usage()
parser.set_defaults(func=info_config)
subsubparsers = parser_config.add_subparsers(help=sc.config)

parser_user = subsubparsers.add_parser('user', help=sc.key_maining_desc)
def info_config_user(args):
    parser_user.print_usage()
parser.set_defaults(func=info_config_user)
subsubsubparsers = parser_user.add_subparsers()

# ### user
parser_add = subsubsubparsers.add_parser('add', help=sc.config_user_add)
parser_add.set_defaults(func=addUser)

parser_del = subsubsubparsers.add_parser('del', help=sc.config_user_del)
parser_del.add_argument('id', type=int, help=sc.config_user_del_id)
parser_del.set_defaults(func=delUser)

parser_list = subsubsubparsers.add_parser('list', help=sc.config_user_list)
parser_list.set_defaults(func=listUser)
# ### user

parser_client = subsubparsers.add_parser('client', help=sc.key_maining_desc)
parser_client.set_defaults(func=createClient)

args = parser.parse_args()
try:
    args.func(args)
except KeyboardInterrupt:
    print()
    print("made rootlol")
db.close()