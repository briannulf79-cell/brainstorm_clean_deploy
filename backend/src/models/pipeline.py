from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime
import json

db = SQLAlchemy()

class Pipeline(db.Model):
    __tablename__ = 'pipelines'
    
    id = db.Column(db.Integer, primary_key=True)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    stages = db.Column(db.Text)  # JSON array of stage objects
    settings = db.Column(db.Text)  # JSON object for pipeline settings
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    opportunities = db.relationship('Opportunity', backref='pipeline', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Pipeline {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'name': self.name,
            'stages': json.loads(self.stages) if self.stages else [],
            'settings': json.loads(self.settings) if self.settings else {},
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'opportunities_count': len(self.opportunities)
        }

class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer, db.ForeignKey('pipelines.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # assigned user
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    stage = db.Column(db.String(100), nullable=False)
    value = db.Column(Numeric(10, 2), default=0)
    probability = db.Column(db.Integer, default=0)  # 0-100 percentage
    expected_close_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='open')  # open, won, lost
    source = db.Column(db.String(100))
    custom_fields = db.Column(db.Text)  # JSON object for custom fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = db.Column(db.DateTime)
    
    # Relationships
    activities = db.relationship('OpportunityActivity', backref='opportunity', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Opportunity {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'pipeline_id': self.pipeline_id,
            'contact_id': self.contact_id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'stage': self.stage,
            'value': float(self.value) if self.value else 0,
            'probability': self.probability,
            'expected_close_date': self.expected_close_date.isoformat() if self.expected_close_date else None,
            'status': self.status,
            'source': self.source,
            'custom_fields': json.loads(self.custom_fields) if self.custom_fields else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'activities_count': len(self.activities)
        }

class OpportunityActivity(db.Model):
    __tablename__ = 'opportunity_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(50), nullable=False)  # stage_change, note, call, email, etc.
    description = db.Column(db.Text)
    old_value = db.Column(db.String(255))  # for tracking changes
    new_value = db.Column(db.String(255))  # for tracking changes
    meta_data = db.Column(db.Text)  # JSON for additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<OpportunityActivity {self.type} for opportunity {self.opportunity_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'opportunity_id': self.opportunity_id,
            'user_id': self.user_id,
            'type': self.type,
            'description': self.description,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'metadata': json.loads(self.meta_data) if self.meta_data else {},
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

