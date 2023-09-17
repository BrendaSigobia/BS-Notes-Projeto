from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = str(request.form.get('email'))
        senha = str(request.form.get('senha'))

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            if check_password_hash(usuario.password, senha):
                flash('Bem vindo!', category='mensagem_de_sucesso')
                login_user(usuario, remember=True)
                return redirect(url_for('views.minhas_notas'))
            else:
                flash('Senha incorreta! Tente novamente.', category='Erro')
        else:
            flash('Email não encontrado. Crie uma conta.', category='Erro')

    return render_template("tela_login.html", usuario=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/cadastro', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = str(request.form.get('email'))
        primeiro_nome = str(request.form.get('primeiroNome'))
        senha1 = str(request.form.get('senha1'))
        senha2 = str(request.form.get('senha2'))

        if db.session.query(Usuario).filter_by(email=email).count() == 1:
            flash('Usuário já existente!', category='Erro')
        elif len(email) < 4:
            flash('Email deve possuir ao menos 4 caractéres.', category='Erro')
        elif len(primeiro_nome) < 2:
            flash('Primeiro nome deve possuir ao menos 2 caractéres.',
                  category='Erro')
        elif senha1 != senha2:
            flash('As senhas devem ser iguais.',
                  category='Erro')
        elif len(senha1) < 7:
            flash('Sua senha deve possuir ao menos 7 caractéres.',
                  category='Erro')
        else:
            novo_usuario = Usuario(email=email, password=generate_password_hash(senha1, method='sha256'),
                                   primeiro_nome=primeiro_nome,)
            db.session.add(novo_usuario)
            db.session.commit()
            login_user(novo_usuario, remember=True)
            flash('Conta criada com sucesso!', category='mensagem_de_sucesso')
            return redirect(url_for('views.minhas_notas'))

    return render_template("tela_cadastro.html",  usuario=current_user)
