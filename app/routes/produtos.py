from flask import render_template, redirect, session, jsonify, request, url_for, make_response, send_file, send_from_directory, Blueprint
from app.routes import produtos_bp
from app.models import Produto, Loja
from app import db
from passlib.hash import bcrypt_sha256
import uuid
import json

@produtos_bp.route("/api/criar-produto", methods=["POST"])
def criarProduto():
  data = request.get_json()
  nome = data["nome"]
  tags = data["tags"]
  price = float(data["price"])
  loja = session['loja']
  vendas = 0
  estoque = data['estoque']

  produto = Produto(str(uuid.uuid4()), nome, tags, price, loja, vendas, estoque)
  db.session.add(produto)
  db.session.commit()

  return jsonify({"message": "Produto criado com sucesso!"})

@produtos_bp.route("/api/editar-produto", methods=["POST"])
def editarProduto():
  data = request.get_json()
  id = data["id"]
  nome = data["nome"]
  tags = data["tags"]
  price = float(data["price"])
  estoque = data["estoque"]

  produto = Produto.query.filter_by(id=id).first()
  produto.nome = nome
  produto.tags = tags
  produto.price = price
  produto.estoque = estoque

  db.session.commit()

  return jsonify({"message": "Produto editado com sucesso!"})

@produtos_bp.route("/api/deletar-produto", methods=["POST"])
def deletarProduto():
  data = request.get_json()
  id = data["id"]

  produto = Produto.query.filter_by(id=id).first()
  db.session.delete(produto)
  db.session.commit()

  return jsonify({"message": "Produto deletado com sucesso!"})

@produtos_bp.route("/api/produtos", methods=["GET"])
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

  return jsonify({"produtos": produtos_json})

@produtos_bp.route("/api/get-produto", methods=["POST"])
def getProduto():
    try:
        data = request.get_json()
        id = data["produto"]

        produto = Produto.query.filter_by(nome=id).first()

        if produto is None:
            raise Exception("Produto não encontrado")

        return jsonify({
            "id": produto.id,
            "nome": produto.nome,
            "tags": produto.tags,
            "price": produto.price,
            "loja": produto.loja,
            "vendas": produto.vendas,
            "estoque": produto.estoque
        })
    except Exception as e:
        print(f"Erro: {str(e)}")
        return jsonify({"error": str(e)}), 404  # Retornar um JSON com o erro e código de status 404