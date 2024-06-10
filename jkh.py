from datetime import datetime, date, timedelta

from flask import Flask
from flask import render_template, url_for

# Получение текущей даты и времени
#now = datetime.now()
# Преобразование даты и времени в строку
#date_str = now.strftime("%Y-%m-%d %H:%M:%S")
# Получение текущей даты
today = date.today()    #+timedelta(days=10)
# Преобразование даты в строку
#date_str = today.strftime("%d.%m.%Y")
date_str = today.strftime("%Y-%m-%d") #  HTML5 требует, чтобы значение для поля ввода типа date было в формате YYYY-MM-DD, независимо от формата, который вы используете при передаче даты из Python/Django
#date_str = today.isoformat()

app = Flask(__name__)

@app.route('/')
def jkh():
    #print( '>>>>>>>>>>>>>>>>>', f"{url_for( 'jkh')=}" )
    menu = ['Водоснабжение', 'Электроэнергия']
    return render_template('index.html', title='Показания', curdate=date_str )

@app.route('/counter')
def counter():
    return render_template('index.html', title='Показания', curdate=date_str)



if __name__ == '__main__':
    app.run( debug=True)