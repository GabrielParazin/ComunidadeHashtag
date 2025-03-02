from fileinput import filename
from multiprocessing.reduction import send_handle

#render template --> conectar o codigo ao HTML

from comunidadeimpressionadora import app,database,bcrypt
from flask import render_template,redirect, flash, url_for,request, abort   #url for pega o nome da funçao
from comunidadeimpressionadora.forms import formLogin, formCriarConta, FormEditarPerfil, Fromcriarpost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required      #current-->verificar o usuario atual #required--> para bloquear visitantes
import secrets
import os
from PIL import Image



@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts = posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios = lista_usuarios)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form_login = formLogin()
    form_criarconta = formCriarConta()


    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):      #verificar se a senha criptografada está correta
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f"Login feito com sucesso para: {form_login.email.data}", 'alert-success')  # data = resultado
            par_next = request.args.get('next')     #pegar o parametro NEXT para direcionar depois do login, so é possivel por causa do request
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
            #return redirect(url_for('home'))
        else:
            flash("E-mail ou senha incorretos", 'alert-danger')


    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f"Conta criada para: {form_criarconta.email.data}", 'alert-primary')
        return redirect(url_for('home'))
    return render_template('login.html', form_login = form_login, form_criarconta = form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash("Saiu da sessão", 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    #local onde está o arquivo de foto
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))  #foto do perfil do cara que tá logado
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods = ['GET', 'POST'])  #toda vez que voce tem um formaulrio com metodo post, o route tem que autorizar  o metodo post
@login_required
def criar_post():
    form = Fromcriarpost()
    if form.validate_on_submit():
        post = Post(titulo = form.titulo.data, corpo = form.corpo.data, autor = current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(6) #adc o codigo ----- vai gerar um codigo
    nome, extensao = os.path.splitext(imagem.filename)    # nome do arquivo e a extensao
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)  # root oath caminho raiz
    tamanho = (400,400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo
    #salvar a imagem


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if "curso_" in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods = ['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    #validate on submit automaticamente vai rodar todas as funçoes que começam com validate_
    if form.validate_on_submit():
        #o e-mail que a gente prencheu no formulario
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash("Perfil atualizado", 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods = ['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = Fromcriarpost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods = ['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluido com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)