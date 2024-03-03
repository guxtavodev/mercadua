from flask import render_template, redirect, session, jsonify, request, url_for, make_response, send_file, send_from_directory, Blueprint
from app.routes import loja_bp
from app.models import Produto, Loja
from app import db
from passlib.hash import bcrypt_sha256
import uuid
import json

def encrypt(dado):
  return bcrypt_sha256.encrypt(dado)

@loja_bp.route("/")
def homepage():
  return render_template("index.html")

@loja_bp.route("/api/criar-loja", methods=["POST"])
def criarLoja():
  nome = request.form['name']
  email = request.form['email']
  senha = request.form['password']
  owner = request.form['owner']
  
  loja = Loja(str(uuid.uuid4()), nome, owner, email, encrypt(senha))
  db.session.add(loja)
  db.session.commit()
  
  return redirect("/")

@loja_bp.route("/api/login", methods=["POST"])
def login():
  email = request.form["email"]
  senha = request.form["password"]

  loja = Loja.query.filter_by(email=email).first()
  if loja and bcrypt_sha256.verify(senha, loja.senha):
    session["loja"] = loja.id
    return redirect("/")
  else:
    return jsonify({"message": "Email ou senha inválidos."})

@loja_bp.route("/api/logout", methods=["GET"])
def logout():
  session.pop("loja", None)
  return redirect("/login")

@loja_bp.route("/settings/<loja>", methods=["GET"])
def settingsPage(loja):
  loja = Loja.query.filter_by(id=loja).first()
  return render_template("settings.html", loja=loja)

@loja_bp.route("/api/exluir-loja/<loja>", methods=["GET"])
def excluirLoja(loja):
  loja = Loja.query.filter_by(id=loja).first()
  db.session.delete(loja)
  db.session.commit()

  for produto in Produto.query.filter_by(loja=loja.id).all():
    db.session.delete(produto)
    db.session.commit()
  return redirect("/")

@loja_bp.route("/api/get-loja/<loja>", methods=["GET"])
def getLoja(loja):
  loja = Loja.query.filter_by(id=loja).first()
  produtos = Produto.query.filter_by(loja=loja).all()
  return jsonify({
    "id": loja.id,
    "nome": loja.nome,
    "owner": loja.owner,
    "email": loja.email,
    "senha": loja.senha,
    "produtos": [{"name": produto.nome, "tags": produto.tags, "price": produto.price, "loja": produto.loja, "vendas": produto.vendas, "estoque": produto.estoque} for produto in produtos]
  })

@loja_bp.route('/produtos')
def listProducts():
  return render_template('produtos.html')