from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    company = db.Column(db.String(255))
    tags = db.Column(db.Text)  # JSON array of tags
    custom_fields = db.Column(db.Text)  # JSON object for custom fields
    status = db.Column(db.String(50), default='active')  # active, inactive, archived
    source = db.Column(db.String(100))  # lead source
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    activities = db.relationship('ContactActivity', backref='contact', lazy=True, cascade='all, delete-orphan')
    notes = db.relationship('ContactNote', backref='contact', lazy=True, cascade='all, delete-orphan')
    tasks = db.relationship('ContactTask', backref='contact', lazy=True, cascade='all, delete-orphan')
    opportunities = db.relationship('Opportunity', backref='contact', lazy=True, cascade='all, delete-orphan')
    conversations = db.relationship('Conversation', backref='contact', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Contact {self.first_name} {self.last_name}>'
    
    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'email': self.email,
            'phone': self.phone,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'company': self.company,
            'tags': json.loads(self.tags) if self.tags else [],
            'custom_fields': json.loads(self.custom_fields) if self.custom_fields else {},
            'status': self.status,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'activities_count': len(self.activities),
            'notes_count': len(self.notes),
            'tasks_count': len(self.tasks)
        }

class ContactActivity(db.Model):
    __tablename__ = 'contact_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(50), nullable=False)  # email, call, sms, meeting, note, etc.
    description = db.Column(db.Text)
    meta_data = db.Column(db.Text)  # JSON for additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactActivity {self.type} for contact {self.contact_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'user_id': self.user_id,
            'type': self.type,
            'description': self.description,
            'metadata': json.loads(self.meta_data) if self.meta_data else {},
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ContactNote(db.Model):
    __tablename__ = 'contact_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactNote for contact {self.contact_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'user_id': self.user_id,
            'content': self.content,
            'is_private': self.is_private,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ContactTask(db.Model):
    __tablename__ = 'contact_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')  # pending, completed, cancelled
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<ContactTask {self.title} for contact {self.contact_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

