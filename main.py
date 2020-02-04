from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime
import requests
from requests import get
import json
import os

dbdir = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/dbMercadoLibre.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class tbl_scraping_merc_libre(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    Titulo = db.Column(db.String(400))
    Precio = db.Column(db.Integer)
    CantPdtosVen = db.Column(db.Integer)
    TipoEnv = db.Column(db.String(10))
    Ciudad = db.Column(db.String(35))   
    FechaCreacion = db.Column(db.DateTime , default= datetime.now)

@app.route('/')
def inicio():
    return render_template("formulario.html")


@app.route('/procesar', methods=['POST','GET'])
def procesar():
    url = ('https://api.mercadolibre.com/sites/MCO/search/')
    nombre =  request.form['nombre']
    edad = request.form['edad']
    args = {'q': nombre, 'limit': edad}
    response = requests.get(url, params=args)
    print(response.url)

    if response.status_code == 200:
        payload = response.json()
        results = payload.get('results', [])
        results=json.loads(response.text)['results']
        if results:
            for results in results:
                title = results['title']
                price = results["price"]
                currency_id = results["currency_id"]
                sold_quantity = results["sold_quantity"]
                city_name = results["address"]["city_name"]
                free_shipping = results["shipping"]["free_shipping"]
                if free_shipping==1:
                    free_shipping = 'Gratis'
                else:
                    free_shipping = 'Se cobra'
                    
                datos = tbl_scraping_merc_libre(Titulo = title,
                                             Precio = price,
                                             CantPdtosVen = sold_quantity,
                                             TipoEnv = free_shipping,
                                             Ciudad = city_name)

                db.session.add(datos)
                db.session.commit()
                
                print(title)
                print(price)
                print(currency_id)
                print(sold_quantity)
                print(city_name)
                print(free_shipping)



                db.session.add(datos)
                db.session.commit

        return render_template("mostrar.html", results=json.loads(response.text)['results'])


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=8082, debug=True)