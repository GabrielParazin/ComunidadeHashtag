#flash = para aparecer mensagem quando validar o login/cadastro
#redirect = redirecionar para uma pagina apos uma ação

from flask import Flask
#from comunidadeimpressionadora.forms import formLogin,formCriarConta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = '70abbb5e00c9f5b1'

#se o codigo estiver rodando no servidor e estiver online, o bd
#é database_url, se noa, o bd vai ser o local
#para manter o codigo tanto pra teste quanto pra prouddçao
if os.getenv("DATABASE_URL"):       #pra pegar uma varivavel de ambiente
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'   #URI --> CAMINHO LOCAL

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'   #direcionar para login quando for visitante
login_manager.login_message_category = 'alert-info'


#criar um engine para avaliar nosso bd
#nspector é para inspecionar a engine
#se naot iver um bd com a tabela usuario nbao serve, entao ja deleta
#tem que importar o models
from comunidadeimpressionadora import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table('usuario'):          #tudo minusculo
    with app.app_context():
        database.drop_all()
        database.create_all()
        print('Criou o BD')
else:
    print('BD já existe')


from comunidadeimpressionadora import routes  #tem que ser depois
