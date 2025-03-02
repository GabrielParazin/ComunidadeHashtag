from flask_wtf import FlaskForm
#imagem filefield abre o popup e a pessoa escolhe o arquivo e sobe ele, allowed== validados quais as extensoes
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

#construir formulario:
#criar pagina, depois criar formulario, depois importa no routes, importa a classe e coloca no render template

#toda pagina com formulario tem que ter metodo post



class formCriarConta(FlaskForm):
    username = StringField('Nome de usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    confirma_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado')

class formLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    #qual label desse campo==field, dentro do fileallowed voce passa uma lista de arquivos (semponto)
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_excel = BooleanField('Excel')
    curso_vba = BooleanField('VBA')
    curso_powerbi = BooleanField('Power BI')
    curso_phyton = BooleanField('Phyton')
    curso_ppt = BooleanField('PPT')
    curso_sql = BooleanField('SQL')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')


    def validate_email(self, email):
        if current_user.email != email.data:
            # verificar se o cara mudou de e-mail
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Existe um usuario com esse e-mail')


class Fromcriarpost(FlaskForm):
    titulo = StringField('Titulo do post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar post')
