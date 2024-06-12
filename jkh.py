from datetime import datetime, date, timedelta

from flask import Flask
from flask import render_template, url_for, request

import sqlite3 as sq
import os
from lib.ini_bd import *

# конфигурация
path_bd = 'e:\data\BD'
DATABASE = os.path.join( path_bd,'meters.db')
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'

conn = sq.connect( DATABASE )

# Получение текущей даты
today = date.today()    #+timedelta(days=10)
# Преобразование даты в строку
date_str = today.strftime("%Y-%m-%d") #  HTML5 требует, чтобы значение для поля ввода типа date было в формате YYYY-MM-DD, независимо от формата, который вы используете при передаче даты из Python/Django

app = Flask(__name__)

@app.route('/')
@app.route('/jkh')
def jkh():
    app.config.from_object(__name__)  # загрузка в конфигурацию параметров (upper)
    #print( '>>>>>>>>>>>>>>>>>', f"{url_for( 'jkh')=}" )
    con = get_db( app )

    menu_adr={'1': 'ул. Марченко',
              '2': 'пр-т Победы'}

    return render_template('index.html', title='ЖКХ', curdate=date_str, menu_adr=menu_adr )

@app.route('/jkh/counter', methods=["POST"])
def counter():
    if request.method == 'POST':
        address = request.form['address']
        lst = request.form['date'].split('-')[::-1]
        date = '.'.join(lst)

        menu_adr = {'1': 'ул. Марченко',
                    '2': 'пр-т Победы'}

    return render_template('counter.html', address=address, date=date, menu_adr=menu_adr )



if __name__ == '__main__':
    app.run( debug=True)