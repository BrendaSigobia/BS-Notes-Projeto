from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)


@views.route('/minhas_notas')
@login_required
def minhas_notas():
    return render_template("notas.html", usuario=current_user)


@views.route('/')
def home():
    return render_template("inicio.html", usuario=current_user)
