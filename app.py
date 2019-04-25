#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for

from data import USERS
# Set API dev in an another file
from api import SITE_API

app = Flask(__name__)
# Add the API
app.register_blueprint(SITE_API)


@app.route('/')
def index():
    app.logger.debug('serving root URL /')
    return render_template('index.html')


@app.route('/indexapi')
def indexapi():
    return render_template('indexapi.html')


@app.route('/users/', methods=['GET', 'POST'])
@app.route('/users/<username>/')
def users(username=None):
    if request.method == 'POST':
       return ajout_data()
      
    if not username:
        return render_template('users.html', users=USERS) # USERS base de données importée liste de dictionnaire avec les informations utilisateurs
    else:
        app.logger.debug(request.args)  # comme un print avec logger python
        info = recherche(USERS, username)
        for i in info.items():
            identif = info['id']
            nom = info['title']
            recipe_link = info['link']
            adresse = info['adresse']
            fields = info['fields']

        # soit on fait un print dans le terminal serveur
        return render_template('usernames.html', infos=info) # Definir un nouveau template username.html
    abort(404)

def ajout_data():
    app.logger.debug(request.args)
    form = request.form
   
    USERS.append(form)
    response = make_response('Ajoute avec succes')
    return render_template('users.html', users=USERS)

def recherche(lst_dico, nom):
    print(lst_dico)
    for dico in lst_dico:
        if nom in dico.values():
            info = dico
    return info

'''
@app.route('/users/')
@app.route('/users/<username>/', methods=['GET'])
def users(username=None):
    if not username:
        return render_template('users.html',users=USERS)
    abort(404) '''


@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    if "pattern" not in request.args :
        return abort(400)
    pattern = request.args.get('pattern')
    print(pattern)    
    req = [u for u in USERS if pattern.lower() in u.get('title').lower()]
#   usrs = [u for u in USERS if pattern.lower() in u.get('name').lower()]
    return render_template('users.html',req1=req)

'''
@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    abort(make_response('Not implemented yet ;)', 501))'''


# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
