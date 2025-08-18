from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # email, sms, mixed
    status = db.Column(db.String(50), default='draft')  # draft, active, paused, completed
    subject = db.Column(db.String(255))  # for email campaigns
    content = db.Column(db.Text)
    template_id = db.Column(db.Integer)
    target_audience = db.Column(db.Text)  # JSON for audience criteria
    schedule_settings = db.Column(db.Text)  # JSON for scheduling
    tracking_settings = db.Column(db.Text)  # JSON for tracking options
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    
    # Relationships
    messages = db.relationship('Message', backref='campaign', lazy=True)
    
    def __repr__(self):
        return f'<Campaign {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'subject': self.subject,
            'content': self.content,
            'template_id': self.template_id,
            'target_audience': json.loads(self.target_audience) if self.target_audience else {},
            'schedule_settings': json.loads(self.schedule_settings) if self.schedule_settings else {},
            'tracking_settings': json.loads(self.tracking_settings) if self.tracking_settings else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'messages_count': len(self.messages)
        }

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    channel = db.Column(db.String(50), nullable=False)  # email, sms, whatsapp, facebook, etc.
    status = db.Column(db.String(50), default='open')  # open, closed, archived
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_message_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Conversation {self.channel} with contact {self.contact_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'channel': self.channel,
            'status': self.status,
            'assigned_user_id': self.assigned_user_id,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'messages_count': len(self.messages)
        }

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))  # if from campaign
    sender_type = db.Column(db.String(20), nullable=False)  # user, contact, system
    sender_id = db.Column(db.Integer)  # user_id if sender_type is user
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50), default='text')  # text, image, file, etc.
    meta_data = db.Column(db.Text)  # JSON for additional data (attachments, etc.)
    status = db.Column(db.String(50), default='sent')  # sent, delivered, read, failed
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Message in conversation {self.conversation_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'campaign_id': self.campaign_id,
            'sender_type': self.sender_type,
            'sender_id': self.sender_id,
            'content': self.content,
            'message_type': self.message_type,
            'metadata': json.loads(self.meta_data) if self.meta_data else {},
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }

