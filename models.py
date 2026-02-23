from database import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    church_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    volunteers = db.relationship("Volunteer", backref="user", lazy=True, cascade="all, delete-orphan")
    schedules = db.relationship("Schedule", backref="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.email}>'


class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.Text, nullable=False)  # JSON string

    def __repr__(self):
        return f'<Volunteer {self.name}>'


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    data = db.Column(db.Text, nullable=False)  # JSON com a escala
    slug = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Schedule {self.slug}>'