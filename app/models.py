from app import app, db

class Loja(db.Model):
  id = db.Column(db.String(), primary_key=True)
  name = db.Column(db.String())
  email = db.Column(db.String())
  senha = db.Column(db.String())

  def __init__(self, id, name, email, senha):
    self.id = id
    self.name = name
    self.email = email
    self.senha = senha

class Produto(db.Model):
  id = db.Column(db.String(), primary_key=True)
  nome = db.Column(db.String())
  tags = db.Column(db.String())
  price = db.Column(db.Float())
  loja = db.Column(db.String()) # ID da Loja
  vendas = db.Column(db.Integer()) # Quantas vezes vendeu o produto
  estoque = db.Column(db.Integer)

  def __init__(self, id, nome, tags, price, loja, vendas, estoque):
    self.id = id
    self.nome = nome
    self.tags = tags
    self.price = price
    self.loja = loja
    self.vendas = vendas
    self.estoque = estoque

class Conta(db.Model):
  nome = db.Column(db.String())
  telefone = db.Column(db.String(), primary_key=True)
  valor = db.Column(db.Float())
  loja = db.Column(db.String())

  def __init__(self, nome, telefone, valor, loja):
    self.nome = nome
    self.telefone = telefone
    self.valor = valor
    self.loja = loja

with app.app_context():
  db.create_all()