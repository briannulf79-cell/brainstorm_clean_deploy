import os
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
import json # Import json at the top for consistency

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    agency_name = Column(String(255))
    role = Column(String(50), default='user')
    subscription_status = Column(String(50), default='trial')
    
    # THE FIX: Set the default value directly in the column definition.
    # This ensures the value is present at the moment of creation.
    trial_expires_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=30))
    
    subscription_expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # The __init__ method is no longer needed as SQLAlchemy handles it.
    
    @property
    def is_trial_expired(self):
        return datetime.utcnow() > self.trial_expires_at
    
    @property
    def is_subscription_active(self):
        # Master users have permanent access
        if self.role == 'master':
            return True
        if self.subscription_status == 'trial':
            return not self.is_trial_expired
        elif self.subscription_status == 'active':
            return self.subscription_expires_at and datetime.utcnow() < self.subscription_expires_at
        return False
    
    @property
    def days_remaining(self):
        if self.role == 'master':
            return 9999 # Master users have effectively infinite days
        if self.subscription_status == 'trial':
            delta = self.trial_expires_at - datetime.utcnow()
            return max(0, delta.days)
        elif self.subscription_status == 'active' and self.subscription_expires_at:
            delta = self.subscription_expires_at - datetime.utcnow()
            return max(0, delta.days)
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'agency_name': self.agency_name,
            'role': self.role,
            'subscription_status': self.subscription_status,
            'is_trial_expired': self.is_trial_expired,
            'is_subscription_active': self.is_subscription_active,
            'days_remaining': self.days_remaining,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key=True)
    sub_account_id = Column(Integer, nullable=False, default=1)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    company = Column(String(255))
    source = Column(String(100))
    status = Column(String(50), default='active')
    tags = Column(Text)
    notes = Column(Text)
    lead_score = Column(Float, default=0.0)
    activities_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def tags_list(self):
        if self.tags:
            try:
                return json.loads(self.tags)
            except:
                return []
        return []
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'source': self.source,
            'status': self.status,
            'tags': self.tags_list,
            'notes': self.notes,
            'lead_score': self.lead_score,
            'activities_count': self.activities_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    plan_name = Column(String(100), nullable=False)
    plan_price = Column(Float, nullable=False)
    billing_cycle = Column(String(20), default='monthly')
    status = Column(String(50), default='active')
    stripe_subscription_id = Column(String(255))
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_name': self.plan_name,
            'plan_price': self.plan_price,
            'billing_cycle': self.billing_cycle,
            'status': self.status,
            'current_period_start': self.current_period_start.isoformat() if self.current_period_start else None,
            'current_period_end': self.current_period_end.isoformat() if self.current_period_end else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
