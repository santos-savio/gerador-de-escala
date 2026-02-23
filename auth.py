from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from database import db, login_manager
from models import User
from utils import hash_password, check_password

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password(password, user.password_hash):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Email ou senha incorretos.', 'error')
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        church_name = request.form.get('church_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validações
        if not church_name or len(church_name) < 3:
            flash('Nome da igreja deve ter pelo menos 3 caracteres.', 'error')
        elif not email or '@' not in email:
            flash('Email inválido.', 'error')
        elif len(password) < 6:
            flash('Senha deve ter pelo menos 6 caracteres.', 'error')
        elif password != confirm_password:
            flash('Senhas não conferem.', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Este email já está cadastrado.', 'error')
        else:
            # Criar usuário
            user = User(
                church_name=church_name,
                email=email,
                password_hash=hash_password(password)
            )
            db.session.add(user)
            db.session.commit()
            
            login_user(user)
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('index'))
    
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('auth.login'))
