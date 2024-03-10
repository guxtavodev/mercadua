from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_cors import CORS

# Crie as instâncias do Flask, SQLAlchemy e LoginManager
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data-2023.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123'
app.config["PERMANENT_SESSION_LIFETIME"] = 3600 * 24 * 7  # 7 dias

db = SQLAlchemy(app)

# Importe e registre as blueprints (rotas) da sua aplicação
from app.routes import produtos_bp, loja_bp, conta_bp
app.register_blueprint(produtos_bp)
app.register_blueprint(loja_bp)
app.register_blueprint(conta_bp)
