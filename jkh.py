from datetime import datetime, date, timedelta

from flask import Flask
from flask import render_template, url_for, request

import sqlite3 as sq
import os
from lib.ini_bd import *
from lib.fdatabase import *


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

    dbase_adr = FDataBase( con, 'address' )
    menu_adr = dbase_adr.getMenu()
    #print( '>>>', dbase_adr.getMenu().items )

    # menu_adr={'1': 'ул. Марченко',
    #           '2': 'пр-т Победы'}

    return render_template('index.html', title='ЖКХ', curdate=date_str, menu_adr=menu_adr )

@app.route('/jkh/counter', methods=["POST","GET"])
def counter():
    print(f"метод: {request.method=}")
    if request.method == 'POST':
        print(f">>>>> {request.form=}, {len(request.form)=}")

        id_adr = int( request.form['address'] )
        con = get_db(app)

        dbase_adr = FDataBase(con, 'address')
        rec_adr = dbase_adr.get_item( id_adr )

        dbase_w = FDataBase(con, 'water')
        rec_w = dbase_w.get_end_date(id_adr)

        dbase_e = FDataBase(con, 'electro')
        rec_e = dbase_e.get_end_date( id_adr, mode="character")
        print( rec_e )

        for k in rec_w.keys():
            print( k, rec_w[k])
        # for k in rec_e.keys():
        #     print( k, rec_e[k])

        dic_pok = { 'date_w':ymd2dmy(rec_w['date']),
                    'val_cold':rec_w['cold'],
                    'val_hot': rec_w['hot'],
                    'date_e': ymd2dmy(rec_e['date']),
                    'val_ed': rec_e['day'],
                    'val_en': rec_e['night'],
                    'val_all': rec_e['all'],
                    'val_te': rec_e['tarif_e']   }

        if 'address' in request.form:
                #address = rec_adr[int(request.form['address'])]
                address = rec_adr['street']
        else:
            print( f"{('address' in request.form)=}")

        if 'date' in request.form:
            lst = request.form['date'].split('-')[::-1]
            date = '.'.join(lst)
        else:
            print( f"{('date' in request.form)=}")

        if len(request.form) > 2: # передача новых показаний на запись
            dbase_w.add_record_water( int(request.form['address']),
                                      request.form['date'],
                                      int(request.form['hot_water']),
                                      int(request.form['cold_water']) )
            dbase_e.add_record_electro( int(request.form['address']),
                                        rec_e['tarif_e'],
                                        request.form['date'],
                                        int(request.form['night_electro']),
                                        int(request.form['day_electro']),
                                        int(request.form['all_electro'])      )

    else:
        print(f'{request.form=} ')

    return render_template('counter.html', address=address, date=date, id_adr=id_adr, **dic_pok )

@app.route('/jkh/viewingreadings', methods=["POST","GET"])
def viewing_reading():
    pass


@app.route('/tables', methods=["POST","GET"])
def tables():
    return render_template('base_meter.html')



if __name__ == '__main__':
    app.run( debug=True)