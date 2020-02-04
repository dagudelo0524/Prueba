
@app.route('/procesar', methods=['POST','GET'])
def procesar():
    url = ('https://api.mercadolibre.com/sites/MLA/search/')
    args = {'q': request.form.get("articulo"), 'limit': request.form.get("cantidad")}


    response = requests.post(url, params=args, json=seller_address)
    print(response.url)


    if response.status_code == 200:
        response_json = json.loads(response.text) #dicionario
        resultado = response_json['results']
        print(resultado)
   
    return render_template("mostrar.html", results=json.loads(response.text)['results'])
    

