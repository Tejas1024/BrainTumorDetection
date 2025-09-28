"""
Database models for brain tumor detection system
Uses SQLAlchemy ORM for database operations
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    """Patient model"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='patient', lazy=True)
    
    def __repr__(self):
        return f'<Patient {self.name}>'

class Doctor(db.Model):
    """Doctor model"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    specialization = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Doctor {self.name}>'

class Prediction(db.Model):
    """Prediction model"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    predicted_class = db.Column(db.Integer, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Prediction {self.id}>'