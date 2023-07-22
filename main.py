from flask import Flask, redirect, request, render_template
from secrets import token_urlsafe

import json

app = Flask(__name__)

urls = {}

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url_longa = request.form['url_longa']
        url_curta = token_urlsafe(5)
       
        while url_curta in urls:
            url_curta = token_urlsafe(5)
            
        urls[url_curta] = url_longa
        with open("urls.json", "w") as f:
            json.dump(urls,f)

        return f"URL Encurtada: {request.url_root}{url_curta}"
    
    return render_template('index.html')


@app.route("/<url_curta>")
def redirect_url(url_curta):
    url_longa = urls.get(url_curta)
    if url_longa:
        return redirect(url_longa)
    else:
        return "erro", 404

with open("urls.json","r") as f:
    urls = json.load(f)

app.run(port=5000,host='localhost',debug=True)
