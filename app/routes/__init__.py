from flask import Blueprint

produtos_bp = Blueprint('produtos', __name__)
loja_bp = Blueprint('loja', __name__)
conta_bp = Blueprint('conta', __name__)

from app.routes import produtos, loja, contas