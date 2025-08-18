from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Agency(db.Model):
    __tablename__ = 'agencies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), unique=True)
    branding_config = db.Column(db.Text)  # JSON string for branding settings
    plan_type = db.Column(db.String(50), default='starter')  # starter, unlimited
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sub_accounts = db.relationship('SubAccount', backref='agency', lazy=True, cascade='all, delete-orphan')
    users = db.relationship('User', backref='agency', lazy=True)
    
    def __repr__(self):
        return f'<Agency {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'branding_config': json.loads(self.branding_config) if self.branding_config else {},
            'plan_type': self.plan_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'sub_accounts_count': len(self.sub_accounts)
        }

class SubAccount(db.Model):
    __tablename__ = 'sub_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(100))
    settings = db.Column(db.Text)  # JSON string for account settings
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contacts = db.relationship('Contact', backref='sub_account', lazy=True, cascade='all, delete-orphan')
    pipelines = db.relationship('Pipeline', backref='sub_account', lazy=True, cascade='all, delete-orphan')
    campaigns = db.relationship('Campaign', backref='sub_account', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SubAccount {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'agency_id': self.agency_id,
            'name': self.name,
            'industry': self.industry,
            'settings': json.loads(self.settings) if self.settings else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'contacts_count': len(self.contacts),
            'pipelines_count': len(self.pipelines)
        }

class UserPermission(db.Model):
    __tablename__ = 'user_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    permissions = db.Column(db.Text)  # JSON string for permissions array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserPermission user_id={self.user_id} sub_account_id={self.sub_account_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'sub_account_id': self.sub_account_id,
            'permissions': json.loads(self.permissions) if self.permissions else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

