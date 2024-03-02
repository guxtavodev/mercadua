from flask import render_template, redirect, session, jsonify, request, url_for, make_response, send_file, send_from_directory, Blueprint
from app.routes import produtos_bp
from app.models import Produto, Loja
from app import db
from passlib.hash import bcrypt_sha256
import uuid
import json

@produtos_bp("/api/criar-produto", methods=["POST"])
def criarProduto():
  data = request.get_json()
  nome = data["nome"]
  tags = data["tags"]
  price = data["price"]
  loja = data["loja"]
  vendas = data["vendas"]
  estoque = data["estoque"]

  produto = Produto(str(uuid.uuid4()), nome, tags, price, loja, vendas, estoque)
  db.session.add(produto)
  db.session.commit()

  return jsonify({"message": "Produto criado com sucesso!"})

@produtos_bp("/api/editar-produto", methods=["POST"])
def editarProduto():
  data = request.get_json()
  id = data["id"]
  nome = data["nome"]
  tags = data["tags"]
  price = data["price"]
  estoque = data["estoque"]

  produto = Produto.query.filter_by(id=id).first()
  produto.nome = nome
  produto.tags = tags
  produto.price = price
  produto.estoque = estoque

  db.session.commit()

  return jsonify({"message": "Produto editado com sucesso!"})

@produtos_bp("/api/deletar-produto", methods=["POST"])
def deletarProduto():
  data = request.get_json()
  id = data["id"]

  produto = Produto.query.filter_by(id=id).first()
  db.session.delete(produto)
  db.session.commit()

  return jsonify({"message": "Produto deletado com sucesso!"})

@produtos_bp("/api/produtos", methods=["GET"])
def getProdutos():
  produtos = Produto.query.all()
  produtos_json = []
  for produto in produtos:
    produtos_json.append({
      "id": produto.id,
      "nome": produto.nome,
      "tags": produto.tags,
      "price": produto.price,
      "loja": produto.loja,
      "vendas": produto.vendas,
      "estoque": produto.estoque
    })

  return jsonify("produtos": produtos_json)

@produtos_bp("/api/get-produto", methods=["GET"])
def getProduto():
  data = request.get_json()
  id = data["id"]

  produto = Produto.query.filter_by(id=id).first()

  return jsonify({
    "id": produto.id,
    "nome": produto.nome,
    "tags": produto.tags,
    "price": produto.price,
    "loja": produto.loja,
    "vendas": produto.vendas,
    "estoque": produto.estoque
  })

