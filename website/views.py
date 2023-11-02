from flask import Blueprint, render_template, request, flash
from .models import Nota
from flask_login import login_required, current_user
from . import db


views = Blueprint('views', __name__)


@views.route('/minhas_notas',  methods=['GET', 'POST'])
@login_required
def minhas_notas():
    if request.method == 'POST':
        nota = str(request.form.get('nota'))

        if len(nota) < 1:
            flash('Preencha sua anotação!', category='Erro')
        else:
            nova_nota = Nota(data=nota, id_usuario=current_user.id)
            db.session.add(nova_nota)
            db.session.commit()
            flash('Anotação salva!', category='mensagem_de_sucesso')

    return render_template("notas.html", usuario=current_user)


@views.route('/')
def home():
    return render_template("inicio.html", usuario=current_user)
