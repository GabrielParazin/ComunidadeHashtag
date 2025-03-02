from comunidadeimpressionadora import database,app
from comunidadeimpressionadora.models import Usuario,Post

# with app.app_context():
#     database.drop_all()
#     database.create_all()
#
# # BANCO TEM SESSAO E COMMIT
#
# with app.app_context():
#     usuario = Usuario(username='Goku', email='goku@gmail.com', senha='123456')
#     usuario2 = Usuario(username='Vegeta', email='vegeta@gmail.com', senha='123456')
#
#     database.session.add(usuario)
#     database.session.add(usuario2)
#
#     database.session.commit()

# with app.app_context():
#     meus_usuarios = Usuario.query.all() #.first
#     usuario_teste = Usuario.query.filter_by(email='goku@gmail.com').first()
#     print(meus_usuarios)
#     print(usuario_teste.posts)

# with app.app_context():
#     post1 = Post(id_usuario=1, titulo='Primeiro Post', corpo='Goku voando')
#     database.session.add(post1)
#     database.session.commit()

# with app.app_context():
#     post = Post.query.first()
#     print(post.autor.email)

with app.app_context():
    usuario = Usuario.query.filter_by(email='gokuSSJ@gmail.com').first()
    print(usuario.cursos)

    post = Post.query.all()
    print(post)