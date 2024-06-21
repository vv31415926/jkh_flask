from datetime import datetime, date, timedelta

from flask import Flask
from flask import render_template, url_for, request, redirect

import sqlite3 as sq
import os
from libprj.ini_bd import *
from libprj.fdatabase import *
from libprj.util import *


# конфигурация
# path_bd = 'e:\data\BD'
# DATABASE = os.path.join( path_bd,'meters.db')
DATABASE = 'meters.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'

conn = sq.connect( DATABASE )

app = Flask(__name__)

menu = [{"name": "Главная",   "url": "jkh"} ]
        # {"name": "Занесение", "url": "counter"},
        # {"name": "История",   "url": "history"}]
#menu = ["Главная","Занесение","История"]

@app.route('/', methods=["POST","GET"])
@app.route('/jkh', methods=["POST","GET"])
def jkh():
    print(f"JKH метод: {request.method=}")
    print( f">>>{request.args.get('link_id')=}")

    today = date.today()  # +timedelta(days=10)
    # Преобразование даты в строку
    tdate = today.strftime("%Y-%m-%d")  # HTML5 требует, чтобы значение для поля ввода типа date было в формате YYYY-MM-DD, независимо от формата, который вы используете при передаче даты из Python/Django
    curdate = ymd2dmy( tdate )
    print( f'jkh: {tdate=},  {curdate=}')  # tdate='2024-06-19',  curdate='19.06.2024'

    endpoint = request.endpoint
    app.config.from_object(__name__)  # загрузка в конфигурацию параметров (upper)
    #print( '>>>>>>>>>>>>>>>>>', f"{url_for( 'jkh')=}" )
    con = get_db( app )

    dbase_adr = FDataBase( con, 'address' )
    sel_addr = dbase_adr.getListAddress()
    #print( '>>>', dbase_adr.getMenu().items )

    # menu_adr={'1': 'ул. Марченко',
    #           '2': 'пр-т Победы'}
    dic = dict(  title='Выбор адреса и даты',
                 meter_date = tdate,
                 menu_adr = sel_addr,
                 curdate = curdate
                 )

    return render_template('index.html', **dic, menu=menu )
# ----------------------------------------------------------------------------------------------------------------

@app.route('/counter', methods=["POST","GET"])
@app.route('/jkh/counter', methods=["POST","GET"])
def counter():
    endpoint = request.endpoint
    #print(f"метод: {request.method=},  {request.endpoint=}")

    if request.method == 'GET':  # из перенаправления
        address_id = int( request.args.get('address_id') )
        meter_date = request.args.get('meter_date')  # '2024-06-19'
    else:
        print( f'Ошибка counter: {request.method=}')

    meter_date = ymd2dmy(meter_date)  # '19.06.2024'

    con = get_db(app)

    dbase_adr = FDataBase(con, 'address')
    rec_adr = dbase_adr.get_item( address_id )

    dbase_w = FDataBase(con, 'water')
    rec_w = dbase_w.get_end_date( address_id )

    dbase_e = FDataBase(con, 'electro')
    rec_e = dbase_e.get_end_date( address_id, mode="character")

    #print( f"{rec_e=}" )
    #print(f"{rec_w=}")

    #for k in rec_w.keys():
    #    print( k, rec_w[k])
    #for k in rec_e.keys():
    #    print( k, rec_e[k])

    # данные из БД - тек состояние показаний
    dic_pok = { 'date_w':ymd2dmy(rec_w['date']), # в БД формат даты: '2024-06-19'
                'val_cold':rec_w['cold'],
                'val_hot': rec_w['hot'],
                'date_e': ymd2dmy(rec_e['date']),  # в БД формат даты: '2024-06-19'
                'val_ed': rec_e['day'],
                'val_en': rec_e['night'],
                'val_all': rec_e['all'],
                'val_te': rec_e['tarif_e'],
                'endpoint': endpoint,
                'name_address': rec_adr['street'],
                'address_id': address_id,
                'meter_date': meter_date
                }
    return render_template('counter.html', **dic_pok, menu=menu )
# ----------------------------------------------------------------------------------------------------------------

@app.route('/jkh/history', methods=["POST","GET"])
def history():
    today = date.today()  # +timedelta(days=10)
    # Преобразование даты в строку
    cur_date = today.strftime("%d.%m.%Y")

    address_idr=0
    if request.method == 'GET':
        address_id = int( request.args.get('address_id') )
    else:
        address_id = int(request.form['address_id'])

    con = get_db( app )
    db_adr = FDataBase(con, 'address')
    rec_adr = db_adr.get_item(address_id)
    name_adr = rec_adr['street']
    # Электроэнергия
    db_e = FDataBase(con, 'electro')
    hist_adr_e = db_e.get_history_electro( address_id )
    # Водоснабжение
    db_w = FDataBase(con, 'water')
    hist_adr_w = db_w.get_history_water(address_id)

    return render_template('history.html', address_name=name_adr, cur_date=cur_date,
                                           lst_adr_e=hist_adr_e,
                                           lst_adr_w=hist_adr_w,
                                            menu=menu)
# ----------------------------------------------------------------------------------------------------------------
@app.route('/jkh/submit_form', methods=['POST'])
@app.route('/submit_form', methods=['POST'])
def submit_form():
    meter_date = request.form['meter_date']
    address_id = request.form['address_id']

    action = request.form['action']

    print( f'submit_form: {meter_date=}, {address_id=}')   # tdate='2024-06-19', address_id='1'

    dic = {   'meter_date': meter_date,
              'address_id': address_id,
    }

    # GET
    if action == 'counter':
        return redirect(  url_for('counter', **dic )    )
    elif action == 'history':
        return redirect(  url_for('history', **dic )   )
    else:
        return redirect(url_for('/'))
# ----------------------------------------------------------------------------------------------------------------
@app.route('/jkh/save_form', methods=['POST'])
@app.route('/save_form', methods=['POST'])
def save_form():
    meter_date = request.form['meter_date']
    address_id = request.form['address_id']
    print( f'{address_id=}, {meter_date=} ' )

    # для перехода на историю
    dic = {   'meter_date': meter_date,
              'address_id': address_id,
    }

    con = get_db(app)
    dbase_w = FDataBase(con, 'water')
    rec_w = dbase_w.get_end_date(address_id)
    dbase_e = FDataBase(con, 'electro')
    rec_e = dbase_e.get_end_date(address_id, mode="character")
    if len(request.form) > 2:  # передача новых показаний на запись
        #       add_record_water(self, adr_id, d, h,c ):
        dbase_w.add_record_water(int(address_id),
                                 meter_date,
                                 int(request.form['hot_water']),
                                 int(request.form['cold_water']))
        dbase_e.add_record_electro(int(address_id),
                                   rec_e['tarif_e'],
                                   meter_date,
                                   int(request.form['night_electro']),
                                   int(request.form['day_electro']),
                                   int(request.form['all_electro']))


    return redirect(  url_for('history', **dic )    )
# ----------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    app.run( debug=True)