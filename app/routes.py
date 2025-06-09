# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Usuario, Veiculo
from functools import wraps
from datetime import datetime # Necessário para converter a data de nascimento

# --- DECORADOR DE ADMIN (adicionado no Passo 2) ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.admin:
            flash('Acesso negado. Você precisa ser um administrador para ver esta página.', 'danger')
            return redirect(url_for('main.listagem'))
        return f(*args, **kwargs)
    return decorated_function

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Usuário logado vai para a listagem, não logado vai para o login
    if current_user.is_authenticated:
        return redirect(url_for('main.listagem'))
    return redirect(url_for('main.login'))

# --- ROTA DE LOGIN (AJUSTADA PARA USAR EMAIL) ---
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.listagem'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            # Redireciona para a página que o usuário tentou acessar antes do login
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.listagem'))
        flash('Email ou senha inválidos', 'danger')
    
    return render_template('login.html')
    
# --- NOVA ROTA: CADASTRO DE USUÁRIO COMUM ---
@main.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario(): # Nome da função alterado
    if current_user.is_authenticated:
        return redirect(url_for('main.listagem'))
        
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        data_nascimento_str = request.form.get('data_nascimento')
        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        email = request.form.get('email')
        password = request.form.get('password')

        if Usuario.query.filter_by(email=email).first():
            flash('Este email já está cadastrado. Tente fazer login.', 'warning')
            return redirect(url_for('main.login'))
            
        new_user = Usuario(
            nome_completo=nome_completo,
            data_nascimento=data_nascimento,
            email=email,
            admin=False
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça seu login.', 'success')
        return redirect(url_for('main.login'))
    
    # Renderiza o template com o novo nome em português
    return render_template('cadastro_usuario.html', title="Cadastro de Usuário")

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.login'))

# --- ROTA PROTEGIDA COM @admin_required ---
@main.route('/cadastro_veiculo', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastro_veiculo():
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
            flash('Veículo cadastrado com sucesso!', 'success')
            return redirect(url_for('main.listagem'))
        except:
            db.session.rollback()
            flash('Erro ao cadastrar veículo. Verifique se a placa já está cadastrada.', 'danger')
    
    return render_template('cadastro_veiculo.html', title="Cadastrar Veículo") # Renomeado para clareza

@main.route('/listagem')
@login_required
def listagem():
    veiculos = Veiculo.query.all()
    # A lógica de admin/comum será feita no template
    return render_template('listagem.html', veiculos=veiculos)

# --- ROTA PROTEGIDA COM @admin_required ---
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
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
            flash('Veículo atualizado com sucesso!', 'success')
            return redirect(url_for('main.listagem'))
        except:
            db.session.rollback()
            flash('Erro ao atualizar veículo. Verifique se a placa já está cadastrada.', 'danger')
    
    return render_template('cadastro_veiculo.html', veiculo=veiculo, title="Editar Veículo")

# --- ROTA PROTEGIDA COM @admin_required ---
# Use POST para exclusão por segurança
@main.route('/excluir/<int:id>', methods=['POST'])
@login_required
@admin_required
def excluir(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    
    try:
        db.session.commit()
        flash('Veículo excluído com sucesso!', 'success')
    except:
        db.session.rollback()
        flash('Erro ao excluir veículo.', 'danger')
    
    return redirect(url_for('main.listagem'))