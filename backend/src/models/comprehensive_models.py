"""
Comprehensive Business Platform Models
All the models needed for the ultimate business platform
"""
import os
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from models import db

# Website Builder & Hosting
class Website(db.Model):
    __tablename__ = 'websites'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    subdomain = Column(String(100), unique=True, nullable=False)  # e.g., 'mybusiness.brainstormaikit.com'
    custom_domain = Column(String(255))  # e.g., 'www.mybusiness.com'
    title = Column(String(255), nullable=False)
    description = Column(Text)
    template_id = Column(String(50))
    content = Column(JSON)  # Store website content/structure
    is_published = Column(Boolean, default=False)
    seo_settings = Column(JSON)
    analytics_code = Column(Text)
    ssl_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="websites")
    
    def to_dict(self):
        return {
            'id': self.id,
            'subdomain': self.subdomain,
            'custom_domain': self.custom_domain,
            'title': self.title,
            'description': self.description,
            'template_id': self.template_id,
            'content': self.content,
            'is_published': self.is_published,
            'seo_settings': self.seo_settings,
            'ssl_enabled': self.ssl_enabled,
            'live_url': f"https://{self.subdomain}.brainstormaikit.com",
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WebsiteTemplate(db.Model):
    __tablename__ = 'website_templates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))  # business, portfolio, ecommerce, etc.
    description = Column(Text)
    thumbnail_url = Column(String(500))
    template_data = Column(JSON)  # HTML/CSS/JS structure
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Sub-Account Management (White Label)
class SubAccount(db.Model):
    __tablename__ = 'sub_accounts'
    
    id = Column(Integer, primary_key=True)
    parent_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    business_name = Column(String(255), nullable=False)
    subdomain = Column(String(100), unique=True)  # e.g., 'client1.youragency.brainstormaikit.com'
    custom_branding = Column(JSON)  # Logo, colors, etc.
    permissions = Column(JSON)  # What features they can access
    billing_settings = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    parent_user = relationship("User", backref="sub_accounts")

# Content Creation & Management
class ContentPiece(db.Model):
    __tablename__ = 'content_pieces'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content_type = Column(String(50))  # blog_post, social_media, video_script, email, etc.
    content = Column(Text)
    ai_generated = Column(Boolean, default=False)
    ai_prompt = Column(Text)
    target_platforms = Column(JSON)  # Where to publish
    scheduled_for = Column(DateTime)
    status = Column(String(50), default='draft')  # draft, scheduled, published
    seo_keywords = Column(JSON)
    engagement_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="content_pieces")

class SocialMediaAccount(db.Model):
    __tablename__ = 'social_media_accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    platform = Column(String(50), nullable=False)  # facebook, instagram, twitter, linkedin, youtube
    account_name = Column(String(255))
    access_token = Column(Text)  # Encrypted
    account_id = Column(String(255))
    is_connected = Column(Boolean, default=False)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="social_accounts")

# Marketing Funnels & Landing Pages
class MarketingFunnel(db.Model):
    __tablename__ = 'marketing_funnels'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    funnel_type = Column(String(100))  # lead_generation, sales, webinar, etc.
    steps = Column(JSON)  # Array of step configurations
    conversion_tracking = Column(JSON)
    a_b_testing = Column(JSON)
    is_active = Column(Boolean, default=False)
    total_visitors = Column(Integer, default=0)
    total_conversions = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="marketing_funnels")

class LandingPage(db.Model):
    __tablename__ = 'landing_pages'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    funnel_id = Column(Integer, ForeignKey('marketing_funnels.id'))
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    template_id = Column(String(50))
    content = Column(JSON)  # Page structure and content
    seo_settings = Column(JSON)
    conversion_elements = Column(JSON)  # Forms, CTAs, etc.
    analytics_data = Column(JSON)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="landing_pages")
    funnel = relationship("MarketingFunnel", backref="landing_pages")

class Survey(db.Model):
    __tablename__ = 'surveys'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    questions = Column(JSON)  # Array of question objects
    settings = Column(JSON)  # Display settings, logic, etc.
    is_published = Column(Boolean, default=False)
    response_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="surveys")

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'
    
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('surveys.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    responses = Column(JSON)  # Question ID -> Answer mapping
    submitted_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    
    # Relationships
    survey = relationship("Survey", backref="responses")

# Enhanced CRM & Customer Profiles
class UnifiedCustomerProfile(db.Model):
    __tablename__ = 'unified_customer_profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)
    
    # Unified data from all touchpoints
    interaction_history = Column(JSON)  # All interactions across channels
    engagement_score = Column(Float, default=0.0)
    lifetime_value = Column(Float, default=0.0)
    preferred_communication = Column(String(50))
    behavioral_data = Column(JSON)
    purchase_history = Column(JSON)
    social_media_profiles = Column(JSON)
    website_activity = Column(JSON)
    email_engagement = Column(JSON)
    
    # AI-generated insights
    personality_profile = Column(JSON)
    predicted_actions = Column(JSON)
    recommended_offers = Column(JSON)
    churn_risk_score = Column(Float, default=0.0)
    
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    contact = relationship("Contact", backref="unified_profile")

# Communication Hub
class Communication(db.Model):
    __tablename__ = 'communications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    channel = Column(String(50), nullable=False)  # email, sms, chat, phone, social
    direction = Column(String(20), nullable=False)  # inbound, outbound
    subject = Column(String(500))
    content = Column(Text)
    status = Column(String(50))  # sent, delivered, read, replied, failed
    thread_id = Column(String(255))  # For grouping related messages
    metadata = Column(JSON)  # Channel-specific data
    scheduled_for = Column(DateTime)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="communications")
    contact = relationship("Contact", backref="communications")

# E-commerce Integration
class Product(db.Model):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    sku = Column(String(100))
    inventory_count = Column(Integer, default=0)
    digital_product = Column(Boolean, default=False)
    download_url = Column(String(500))  # For digital products
    images = Column(JSON)  # Array of image URLs
    categories = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="products")

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    order_number = Column(String(100), unique=True, nullable=False)
    status = Column(String(50), default='pending')  # pending, paid, shipped, delivered, cancelled
    total_amount = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    payment_status = Column(String(50))
    payment_method = Column(String(100))
    stripe_payment_intent_id = Column(String(255))
    items = Column(JSON)  # Order items with quantities
    shipping_address = Column(JSON)
    billing_address = Column(JSON)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="orders")
    contact = relationship("Contact", backref="orders")

# Analytics & Reporting
class AnalyticsEvent(db.Model):
    __tablename__ = 'analytics_events'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_type = Column(String(100), nullable=False)  # page_view, click, conversion, etc.
    event_data = Column(JSON)
    source = Column(String(100))  # website, email, social, etc.
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    session_id = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="analytics_events")

# Automation & Workflows
class Automation(db.Model):
    __tablename__ = 'automations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    trigger_type = Column(String(100))  # form_submission, email_open, page_visit, etc.
    trigger_conditions = Column(JSON)
    workflow_steps = Column(JSON)  # Array of action objects
    is_active = Column(Boolean, default=False)
    execution_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="automations")

class AutomationExecution(db.Model):
    __tablename__ = 'automation_executions'
    
    id = Column(Integer, primary_key=True)
    automation_id = Column(Integer, ForeignKey('automations.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    status = Column(String(50))  # running, completed, failed
    execution_log = Column(JSON)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    automation = relationship("Automation", backref="executions")
    contact = relationship("Contact")