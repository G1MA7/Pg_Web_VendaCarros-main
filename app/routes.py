from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Usuario, Veiculo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.listagem'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.listagem'))
        flash('Usuário ou senha inválidos')
    
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro():
    if request.method == 'POST':
        modelo = request.form.get('modelo')
        marca = request.form.get('marca')
        ano = request.form.get('ano')
        placa = request.form.get('placa')
        cor = request.form.get('cor')
        
        veiculo = Veiculo(modelo=modelo, marca=marca, ano=ano, placa=placa, cor=cor)
        db.session.add(veiculo)
        
        try:
            db.session.commit()
            flash('Veículo cadastrado com sucesso!')
            return redirect(url_for('main.listagem'))
        except:
            db.session.rollback()
            flash('Erro ao cadastrar veículo. Verifique se a placa já está cadastrada.')
    
    return render_template('cadastro.html')

@main.route('/listagem')
@login_required
def listagem():
    veiculos = Veiculo.query.all()
    return render_template('listagem.html', veiculos=veiculos)

@main.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    veiculo = Veiculo.query.get_or_404(id)
    
    if request.method == 'POST':
        veiculo.modelo = request.form.get('modelo')
        veiculo.marca = request.form.get('marca')
        veiculo.ano = request.form.get('ano')
        veiculo.placa = request.form.get('placa')
        veiculo.cor = request.form.get('cor')
        
        try:
            db.session.commit()
            flash('Veículo atualizado com sucesso!')
            return redirect(url_for('main.listagem'))
        except:
            db.session.rollback()
            flash('Erro ao atualizar veículo. Verifique se a placa já está cadastrada.')
    
    return render_template('cadastro.html', veiculo=veiculo)

@main.route('/excluir/<int:id>')
@login_required
def excluir(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    
    try:
        db.session.commit()
        flash('Veículo excluído com sucesso!')
    except:
        db.session.rollback()
        flash('Erro ao excluir veículo.')
    
    return redirect(url_for('main.listagem'))