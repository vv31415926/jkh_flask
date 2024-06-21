import sqlite3 as sq
from flask import Flask, g

def connect_db( app:Flask ):
    '''
    Установление соединения с БД в режиме словаря
    '''
    conn = sq.connect( app.config['DATABASE'] )
    conn.row_factory = sq.Row  # представить записи из БД в виде словаря, а не кортежа
    return conn

def create_db( app:Flask ):
    """
    Вспомогательная функция для создания таблиц БД
    создание структуры БД без запуска вэб-сервера
    """
    db = connect_db()
    with app.open_resource( 'sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db( app ):
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr( g, 'link_db'):
        g.link_db = connect_db( app )
    return g.link_db

# sq_db.sql:
# create table if not exists mainmenu (
# id integer primary key autoincrement,
# title text not null,
# url text not null
# );
# CREATE TABLE users (
#             name TEXT,
#             ava BLOB,
#             score INTEGER);
# INSERT INTO "users" VALUES('Николай', …,1000);