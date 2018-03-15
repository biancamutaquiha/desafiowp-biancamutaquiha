from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = 'notsecretkey'

from models.tables import Compra, Produto, Base

engine = create_engine('sqlite:///estoque.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/home')
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    
    if request.method == 'POST':
        nome = request.form['produto'].strip().capitalize() 
        if nome:
            try:
                session.add(Produto(nome=nome)) 
                session.commit()
                flash('O produto {} foi cadastrado com sucesso'.format(nome), 'success')
            except:
                session.rollback()
                flash('Erro: o produto {} já está cadastrado na lista de produtos'.format(nome), 'danger')

        return redirect(url_for('produtos'))
  
    lista_produtos = session.query(Produto).all() 
    return render_template('produtos.html', lista_produtos=lista_produtos)

@app.route('/compras', methods=['GET', 'POST'])
def compras():
        
    if request.method == 'POST':
        produto = request.form['produto'].strip().capitalize()
        quantidade = request.form['quantidade']
        preco  = request.form['preco']
        
        if produto and quantidade and preco:
            preco_medio = round(float(preco) / int(quantidade), 2)
            try: 
                session.add(Compra(produto=produto, quantidade=quantidade, preco=preco, preco_medio=preco_medio))
                session.commit()
                flash('Compra de {} adicionada com sucesso'.format(produto))
            except:
                session.rollback()

        return redirect(url_for('compras'))

    lista_produtos = session.query(Produto).all()
    lista_compras = session.query(Compra).all()
    
    return render_template('compras.html', lista_compras=lista_compras , lista_produtos=lista_produtos)

if __name__ == '__main__':
    app.run(debug=True)