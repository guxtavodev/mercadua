from os import replace
from flask import render_template, redirect, session, jsonify, request, url_for, make_response, send_file, send_from_directory, Blueprint
from app.routes import conta_bp
from app.models import Produto, Loja, Conta
from app import db
from passlib.hash import bcrypt_sha256
import uuid
import json

@conta_bp.route('/api/criar-conta', methods=['POST'])
def criarContaCliente():
  data = request.get_json()
  nome = data['nome']
  telefone = data['telefone']
  valor = data['valor']
  conta = Conta(nome, telefone, float(valor), session['loja'])
  db.session.add(conta)
  db.session.commit()
  return jsonify({'message': 'Conta criada com sucesso!'})

@conta_bp.route("/api/add-valor", methods=['POST'])
def addValorConta():
  data = request.get_json()
  conta = Conta.query.filter_by(nome=data['nome']).first()
  conta.valor += float(data['valor'])
  db.session.commit()
  return jsonify({'message': 'Valor adicionado com sucesso!'})

@conta_bp.route("/api/remove-valor", methods=['POST'])
def removeValorConta():
  data = request.get_json()
  conta = Conta.query.filter_by(nome=data['nome']).first()
  conta.valor -= float(data['valor'])
  db.session.commit()
  return jsonify({'message': 'Valor removido com sucesso!'})

@conta_bp.route("/api/get-conta", methods=['GET'])
def getConta():
  conta = Conta.query.filter_by(id=request.args.get('id')).first()
  return jsonify(conta.to_dict())

@conta_bp.route('/api/excluir-conta', methods=['POST'])
def excluirConta():
  data = request.get_json()
  conta = Conta.query.filter_by(id=data['id']).first()
  db.session.delete(conta)
  db.session.commit()
  return jsonify({'message': 'Conta excluída com sucesso!'})

