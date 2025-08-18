from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from src.models.user import db
import enum

class MessageType(enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    CALL = "call"
    CHAT = "chat"
    VOICEMAIL = "voicemail"

class MessageDirection(enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class ConversationStatus(enum.Enum):
    OPEN = "open"
    PENDING = "pending"
    CLOSED = "closed"
    ARCHIVED = "archived"

class MessageStatus(enum.Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    PENDING = "pending"

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    sub_account_id = Column(Integer, ForeignKey('sub_accounts.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)
    
    # Conversation details
    type = Column(Enum(MessageType), nullable=False)
    status = Column(Enum(ConversationStatus), default=ConversationStatus.OPEN)
    subject = Column(String(255))
    
    # Assignment and tracking
    assigned_to_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_message_at = Column(DateTime)
    
    # Metrics
    unread_count = Column(Integer, default=0)
    message_count = Column(Integer, default=0)
    
    # AI Analysis
    ai_sentiment = Column(String(50))  # positive, negative, neutral
    ai_priority = Column(String(50))   # high, medium, low
    ai_intent = Column(String(100))    # demo_request, support, pricing, etc.
    ai_summary = Column(Text)
    
    # Tags and metadata
    tags = Column(JSON)
    custom_fields = Column(JSON)
    
    # Relationships
    contact = relationship("Contact", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    assigned_to = relationship("User")
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'contact_id': self.contact_id,
            'type': self.type.value if self.type else None,
            'status': self.status.value if self.status else None,
            'subject': self.subject,
            'assigned_to_id': self.assigned_to_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'unread_count': self.unread_count,
            'message_count': self.message_count,
            'ai_sentiment': self.ai_sentiment,
            'ai_priority': self.ai_priority,
            'ai_intent': self.ai_intent,
            'ai_summary': self.ai_summary,
            'tags': self.tags or [],
            'custom_fields': self.custom_fields or {},
            'contact': self.contact.to_dict() if self.contact else None,
            'assigned_to': {
                'id': self.assigned_to.id,
                'first_name': self.assigned_to.first_name,
                'last_name': self.assigned_to.last_name,
                'email': self.assigned_to.email
            } if self.assigned_to else None
        }

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    
    # Message details
    type = Column(Enum(MessageType), nullable=False)
    direction = Column(Enum(MessageDirection), nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.PENDING)
    
    # Content
    subject = Column(String(255))
    content = Column(Text)
    html_content = Column(Text)
    
    # Sender/Recipient info
    from_address = Column(String(255))  # email or phone number
    to_address = Column(String(255))    # email or phone number
    from_name = Column(String(255))
    to_name = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    read_at = Column(DateTime)
    
    # Call-specific fields
    call_duration = Column(Integer)  # in seconds
    call_recording_url = Column(String(500))
    call_status = Column(String(50))  # answered, missed, busy, etc.
    
    # Email-specific fields
    email_message_id = Column(String(255))
    email_thread_id = Column(String(255))
    
    # SMS-specific fields
    sms_message_id = Column(String(255))
    sms_segments = Column(Integer, default=1)
    
    # Attachments and media
    attachments = Column(JSON)  # List of attachment URLs/info
    
    # AI Analysis
    ai_sentiment = Column(String(50))
    ai_intent = Column(String(100))
    ai_entities = Column(JSON)  # Extracted entities (names, dates, etc.)
    ai_summary = Column(Text)
    
    # Metadata
    custom_fields = Column(JSON)
    external_id = Column(String(255))  # ID from external service
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'type': self.type.value if self.type else None,
            'direction': self.direction.value if self.direction else None,
            'status': self.status.value if self.status else None,
            'subject': self.subject,
            'content': self.content,
            'html_content': self.html_content,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'from_name': self.from_name,
            'to_name': self.to_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'call_duration': self.call_duration,
            'call_recording_url': self.call_recording_url,
            'call_status': self.call_status,
            'email_message_id': self.email_message_id,
            'email_thread_id': self.email_thread_id,
            'sms_message_id': self.sms_message_id,
            'sms_segments': self.sms_segments,
            'attachments': self.attachments or [],
            'ai_sentiment': self.ai_sentiment,
            'ai_intent': self.ai_intent,
            'ai_entities': self.ai_entities or {},
            'ai_summary': self.ai_summary,
            'custom_fields': self.custom_fields or {},
            'external_id': self.external_id
        }

class EmailAccount(db.Model):
    __tablename__ = 'email_accounts'
    
    id = Column(Integer, primary_key=True)
    sub_account_id = Column(Integer, ForeignKey('sub_accounts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Account details
    email_address = Column(String(255), nullable=False)
    display_name = Column(String(255))
    
    # SMTP Configuration
    smtp_host = Column(String(255))
    smtp_port = Column(Integer)
    smtp_username = Column(String(255))
    smtp_password = Column(String(255))  # Should be encrypted
    smtp_use_tls = Column(Boolean, default=True)
    smtp_use_ssl = Column(Boolean, default=False)
    
    # IMAP Configuration
    imap_host = Column(String(255))
    imap_port = Column(Integer)
    imap_username = Column(String(255))
    imap_password = Column(String(255))  # Should be encrypted
    imap_use_ssl = Column(Boolean, default=True)
    
    # Status and settings
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    auto_sync = Column(Boolean, default=True)
    sync_frequency = Column(Integer, default=5)  # minutes
    
    # OAuth settings (for Gmail, Outlook, etc.)
    oauth_provider = Column(String(50))
    oauth_access_token = Column(Text)
    oauth_refresh_token = Column(Text)
    oauth_expires_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_sync_at = Column(DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'user_id': self.user_id,
            'email_address': self.email_address,
            'display_name': self.display_name,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'auto_sync': self.auto_sync,
            'sync_frequency': self.sync_frequency,
            'oauth_provider': self.oauth_provider,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_sync_at': self.last_sync_at.isoformat() if self.last_sync_at else None
        }

class SMSAccount(db.Model):
    __tablename__ = 'sms_accounts'
    
    id = Column(Integer, primary_key=True)
    sub_account_id = Column(Integer, ForeignKey('sub_accounts.id'), nullable=False)
    
    # Account details
    phone_number = Column(String(20), nullable=False)
    display_name = Column(String(255))
    
    # Provider configuration
    provider = Column(String(50))  # twilio, messagebird, etc.
    account_sid = Column(String(255))
    auth_token = Column(String(255))  # Should be encrypted
    api_key = Column(String(255))
    api_secret = Column(String(255))  # Should be encrypted
    
    # Settings
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    webhook_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'phone_number': self.phone_number,
            'display_name': self.display_name,
            'provider': self.provider,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'webhook_url': self.webhook_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CallAccount(db.Model):
    __tablename__ = 'call_accounts'
    
    id = Column(Integer, primary_key=True)
    sub_account_id = Column(Integer, ForeignKey('sub_accounts.id'), nullable=False)
    
    # Account details
    phone_number = Column(String(20), nullable=False)
    display_name = Column(String(255))
    
    # Provider configuration
    provider = Column(String(50))  # twilio, vonage, etc.
    account_sid = Column(String(255))
    auth_token = Column(String(255))  # Should be encrypted
    api_key = Column(String(255))
    api_secret = Column(String(255))  # Should be encrypted
    
    # Call settings
    recording_enabled = Column(Boolean, default=True)
    transcription_enabled = Column(Boolean, default=True)
    voicemail_enabled = Column(Boolean, default=True)
    call_forwarding_number = Column(String(20))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    webhook_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'phone_number': self.phone_number,
            'display_name': self.display_name,
            'provider': self.provider,
            'recording_enabled': self.recording_enabled,
            'transcription_enabled': self.transcription_enabled,
            'voicemail_enabled': self.voicemail_enabled,
            'call_forwarding_number': self.call_forwarding_number,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'webhook_url': self.webhook_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Add relationships to existing models
def add_communication_relationships():
    """Add communication relationships to existing models"""
    from src.models.contact import Contact
    from src.models.user import User
    
    # Add conversations relationship to Contact
    if not hasattr(Contact, 'conversations'):
        Contact.conversations = relationship("Conversation", back_populates="contact")

