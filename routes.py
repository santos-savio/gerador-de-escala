from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from database import db
from models import Volunteer, Schedule
from utils import generate_unique_slug
from datetime import datetime
import json

api = Blueprint('api', __name__)

# ==================== VOLUNTÁRIOS ====================

@api.route('/api/volunteers', methods=['GET'])
@login_required
def get_volunteers():
    """Lista todos os voluntários do usuário"""
    volunteers = Volunteer.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'availability': json.loads(v.availability)
    } for v in volunteers])

@api.route('/api/volunteers', methods=['POST'])
@login_required
def add_volunteer():
    """Adiciona um novo voluntário"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Nome é obrigatório'}), 400
    
    volunteer = Volunteer(
        user_id=current_user.id,
        name=data['name'],
        availability=json.dumps(data.get('availability', []))
    )
    
    db.session.add(volunteer)
    db.session.commit()
    
    return jsonify({
        'id': volunteer.id,
        'name': volunteer.name,
        'availability': json.loads(volunteer.availability)
    }), 201

@api.route('/api/volunteers/<int:volunteer_id>', methods=['PUT'])
@login_required
def update_volunteer(volunteer_id):
    """Atualiza um voluntário"""
    volunteer = Volunteer.query.filter_by(id=volunteer_id, user_id=current_user.id).first()
    
    if not volunteer:
        return jsonify({'error': 'Voluntário não encontrado'}), 404
    
    data = request.get_json()
    
    if data.get('name'):
        volunteer.name = data['name']
    if 'availability' in data:
        volunteer.availability = json.dumps(data['availability'])
    
    db.session.commit()
    
    return jsonify({
        'id': volunteer.id,
        'name': volunteer.name,
        'availability': json.loads(volunteer.availability)
    })

@api.route('/api/volunteers/<int:volunteer_id>', methods=['DELETE'])
@login_required
def delete_volunteer(volunteer_id):
    """Remove um voluntário"""
    volunteer = Volunteer.query.filter_by(id=volunteer_id, user_id=current_user.id).first()
    
    if not volunteer:
        return jsonify({'error': 'Voluntário não encontrado'}), 404
    
    db.session.delete(volunteer)
    db.session.commit()
    
    return jsonify({'message': 'Voluntário removido com sucesso'})

# ==================== ESCALAS ====================

@api.route('/api/schedules', methods=['GET'])
@login_required
def get_schedules():
    """Lista todas as escalas do usuário"""
    schedules = Schedule.query.filter_by(user_id=current_user.id).order_by(Schedule.created_at.desc()).all()
    return jsonify([{
        'id': s.id,
        'department': s.department,
        'period_start': s.period_start.isoformat(),
        'period_end': s.period_end.isoformat(),
        'data': json.loads(s.data),
        'slug': s.slug,
        'created_at': s.created_at.isoformat()
    } for s in schedules])

@api.route('/api/schedules', methods=['POST'])
@login_required
def create_schedule():
    """Cria uma nova escala"""
    data = request.get_json()
    
    if not data.get('department') or not data.get('period_start') or not data.get('period_end'):
        return jsonify({'error': 'Departamento e período são obrigatórios'}), 400
    
    # Gera slug único
    slug = generate_unique_slug()
    while Schedule.query.filter_by(slug=slug).first():
        slug = generate_unique_slug()
    
    schedule = Schedule(
        user_id=current_user.id,
        department=data['department'],
        period_start=datetime.fromisoformat(data['period_start']).date(),
        period_end=datetime.fromisoformat(data['period_end']).date(),
        data=json.dumps(data.get('data', {})),
        slug=slug
    )
    
    db.session.add(schedule)
    db.session.commit()
    
    return jsonify({
        'id': schedule.id,
        'slug': schedule.slug,
        'message': 'Escala salva com sucesso'
    }), 201

@api.route('/api/schedules/<int:schedule_id>', methods=['DELETE'])
@login_required
def delete_schedule(schedule_id):
    """Remove uma escala"""
    schedule = Schedule.query.filter_by(id=schedule_id, user_id=current_user.id).first()
    
    if not schedule:
        return jsonify({'error': 'Escala não encontrada'}), 404
    
    db.session.delete(schedule)
    db.session.commit()
    
    return jsonify({'message': 'Escala removida com sucesso'})

# ==================== ROTA PÚBLICA ====================

@api.route('/escala/<slug>')
def view_schedule(slug):
    """Visualização pública da escala com OG tags"""
    schedule = Schedule.query.filter_by(slug=slug).first_or_404()
    
    # Busca nome da igreja
    church_name = schedule.user.church_name
    
    # Dados da escala
    schedule_data = json.loads(schedule.data)
    
    # Imagem do departamento para OG
    dept_images = {
        'mesa-som': 'mesa-som.png',
        'sabatina': 'sabatina.png',
        'pregacao': 'pregacao.jpg',
        'louvor': 'louvor.png',
        'recepcao': 'recepcao.jpg',
        'diácono': 'diacono.jpg',
        'limpeza': 'limpeza.jpeg',
        'infantil': 'infantil.jpg'
    }
    
    dept_key = schedule.department.lower().replace(' ', '-').replace('á', 'a')
    og_image = f"/IMG/{dept_images.get(dept_key, 'louvor.png')}"
    
    return render_template('escala_publica.html',
        schedule=schedule,
        schedule_data=schedule_data,
        church_name=church_name,
        og_image=og_image
    )
