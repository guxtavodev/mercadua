from flask import render_template, redirect, session, jsonify, request, Blueprint
from app.routes import conta_bp
from app.models import Produto, Loja, Conta
from app import db
from passlib.hash import bcrypt_sha256
import uuid
import json
from sqlalchemy import func

@conta_bp.route('/api/criar-conta', methods=['POST'])
def criarContaCliente():
    data = request.get_json()
    nome = data['nome']
    telefone = data['telefone']
    valor = data['valor']
    loja = session.get('loja')  # Obter o nome da loja da sessão
    conta = Conta(nome, telefone, float(valor), loja)
    db.session.add(conta)
    db.session.commit()
    return jsonify({'message': 'Conta criada com sucesso!'})

@conta_bp.route("/api/add-valor", methods=['POST'])
def addValorConta():
    data = request.get_json()
    nome = data['nome'].lower()  # Convertendo o nome para minúsculas
    valor = float(data['valor'])
    loja = session.get('loja')  # Obter o nome da loja da sessão


    conta = Conta.query.filter(func.lower(Conta.nome) == nome, func.lower(Conta.loja) == loja).first()

    if conta:
        conta.valor += valor
        db.session.commit()
        return jsonify({'message': 'Valor adicionado com sucesso!'})
    else:
        return jsonify({'error': 'Conta não encontrada.'}), 404


@conta_bp.route("/api/remove-valor", methods=['POST'])
def removeValorConta():
    data = request.get_json()
    nome = data['nome'].lower()
    valor = float(data['valor'])
    loja = session.get('loja')  # Obter o nome da loja da sessão
    conta = Conta.query.filter(func.lower(Conta.nome) == nome, func.lower(Conta.loja) == loja).first()
    if conta:
        conta.valor -= valor
        db.session.commit()
        return jsonify({'message': 'Valor removido com sucesso!'})
    else:
        return jsonify({'error': 'Conta não encontrada.'}), 404

@conta_bp.route("/api/get-conta", methods=['GET'])
def getConta():
    loja = session.get('loja')  # Obter o nome da loja da sessão
    nome_conta = request.args.get('nome')
    conta = Conta.query.filter_by(nome=nome_conta, loja=loja).first()
    if conta:
        return jsonify(conta.to_dict())
    else:
        return jsonify({'error': 'Conta não encontrada.'}), 404

@conta_bp.route('/api/excluir-conta/<conta>', methods=['GET'])
def excluirConta(conta):
    loja = session.get('loja')  # Obter o nome da loja da sessão
    conta = Conta.query.filter_by(nome=conta, loja=loja).first()
    if conta:
        db.session.delete(conta)
        db.session.commit()
        return redirect('/produtos')
    else:
        return jsonify({'error': 'Conta não encontrada.'}), 404
