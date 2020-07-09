import sqlite3
import json
import time
from threading import Timer
from telethon import TelegramClient

from flask import Flask

app = Flask(__name__)

def telegranGetBalance():
    global balance
    db = sqlite3.connect('Account.db')
    cur = db.cursor()
    balanceTemp = {
        "all": 0,
        "users": [
        ]
    }
    x = 1  # це счетчик
    for item in cur.fetchall():
        session = "anon" + str(x)
        print(session, item[4], item[5])
        client = TelegramClient(session, item[4], item[5])
        client.start()

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
            print(qq)
            waitin = float(qq)

        balanceTemp["users"].append({"user": item[3], "balance": waitin})
        balanceTemp["all"] = balanceTemp["all"] + waitin
        x = x + 1  # це конкатенация счетчика
    balance = balanceTemp
    cur.close()
    db.close()


@app.route('/')
def index():
    return 'it is api bro'

@app.route('/balance')
def getBalance():
    global balance
    return json.dumps(balance)

if __name__ == '__main__':
    t = Timer(30.0, telegranGetBalance)
    t.start()
    app.run(host="0.0.0.0", port=80)
