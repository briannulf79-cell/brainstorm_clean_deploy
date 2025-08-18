from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime
import json

db = SQLAlchemy()

class Integration(db.Model):
    __tablename__ = 'integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # zapier, google_ads, facebook_ads, etc.
    type = db.Column(db.String(50), nullable=False)  # crm, marketing, payment, communication, etc.
    status = db.Column(db.String(20), default='active')  # active, inactive, error
    config = db.Column(db.Text)  # JSON configuration
    credentials = db.Column(db.Text)  # Encrypted credentials
    webhook_url = db.Column(db.String(500))
    last_sync_at = db.Column(db.DateTime)
    sync_frequency = db.Column(db.String(20), default='hourly')  # realtime, hourly, daily
    error_count = db.Column(db.Integer, default=0)
    last_error = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Integration {self.name} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'config': json.loads(self.config) if self.config else {},
            'webhook_url': self.webhook_url,
            'last_sync_at': self.last_sync_at.isoformat() if self.last_sync_at else None,
            'sync_frequency': self.sync_frequency,
            'error_count': self.error_count,
            'last_error': self.last_error,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WebsiteBuilder(db.Model):
    __tablename__ = 'websites'
    
    id = db.Column(db.Integer, primary_key=True)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255))
    subdomain = db.Column(db.String(100))  # agileaisolutions subdomain
    template_id = db.Column(db.String(50))
    pages = db.Column(db.Text)  # JSON array of pages
    theme_config = db.Column(db.Text)  # JSON theme configuration
    seo_config = db.Column(db.Text)  # JSON SEO settings
    analytics_config = db.Column(db.Text)  # JSON analytics settings
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    ssl_enabled = db.Column(db.Boolean, default=True)
    performance_score = db.Column(db.Integer)  # 0-100 performance score
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    forms = db.relationship('WebsiteForm', backref='website', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Website {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'name': self.name,
            'domain': self.domain,
            'subdomain': self.subdomain,
            'template_id': self.template_id,
            'pages': json.loads(self.pages) if self.pages else [],
            'theme_config': json.loads(self.theme_config) if self.theme_config else {},
            'seo_config': json.loads(self.seo_config) if self.seo_config else {},
            'analytics_config': json.loads(self.analytics_config) if self.analytics_config else {},
            'status': self.status,
            'ssl_enabled': self.ssl_enabled,
            'performance_score': self.performance_score,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'forms_count': len(self.forms)
        }

class WebsiteForm(db.Model):
    __tablename__ = 'website_forms'
    
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('websites.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    form_fields = db.Column(db.Text)  # JSON array of form fields
    settings = db.Column(db.Text)  # JSON form settings
    redirect_url = db.Column(db.String(500))
    thank_you_message = db.Column(db.Text)
    notification_emails = db.Column(db.Text)  # JSON array of emails
    automation_trigger = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = db.relationship('FormSubmission', backref='form', lazy=True)
    
    def __repr__(self):
        return f'<WebsiteForm {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'website_id': self.website_id,
            'name': self.name,
            'form_fields': json.loads(self.form_fields) if self.form_fields else [],
            'settings': json.loads(self.settings) if self.settings else {},
            'redirect_url': self.redirect_url,
            'thank_you_message': self.thank_you_message,
            'notification_emails': json.loads(self.notification_emails) if self.notification_emails else [],
            'automation_trigger': self.automation_trigger,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'submissions_count': len(self.submissions)
        }

class FormSubmission(db.Model):
    __tablename__ = 'form_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('website_forms.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))  # linked contact if created
    submission_data = db.Column(db.Text)  # JSON form data
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    referrer = db.Column(db.String(500))
    utm_source = db.Column(db.String(100))
    utm_medium = db.Column(db.String(100))
    utm_campaign = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<FormSubmission form_id={self.form_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'form_id': self.form_id,
            'contact_id': self.contact_id,
            'submission_data': json.loads(self.submission_data) if self.submission_data else {},
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'utm_source': self.utm_source,
            'utm_medium': self.utm_medium,
            'utm_campaign': self.utm_campaign,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class OnlineCourse(db.Model):
    __tablename__ = 'online_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    thumbnail_url = db.Column(db.String(500))
    price = db.Column(Numeric(10, 2), default=0)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    access_type = db.Column(db.String(20), default='paid')  # free, paid, membership
    drip_content = db.Column(db.Boolean, default=False)
    certificate_enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lessons = db.relationship('CourseLesson', backref='course', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('CourseEnrollment', backref='course', lazy=True)
    
    def __repr__(self):
        return f'<OnlineCourse {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'title': self.title,
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'price': float(self.price) if self.price else 0,
            'currency': self.currency,
            'status': self.status,
            'access_type': self.access_type,
            'drip_content': self.drip_content,
            'certificate_enabled': self.certificate_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'lessons_count': len(self.lessons),
            'enrollments_count': len(self.enrollments)
        }

class CourseLesson(db.Model):
    __tablename__ = 'course_lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('online_courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)  # HTML content
    video_url = db.Column(db.String(500))
    duration_minutes = db.Column(db.Integer)
    order_index = db.Column(db.Integer, default=0)
    is_preview = db.Column(db.Boolean, default=False)
    drip_days = db.Column(db.Integer, default=0)  # days after enrollment to unlock
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CourseLesson {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'video_url': self.video_url,
            'duration_minutes': self.duration_minutes,
            'order_index': self.order_index,
            'is_preview': self.is_preview,
            'drip_days': self.drip_days,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CourseEnrollment(db.Model):
    __tablename__ = 'course_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('online_courses.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    progress_percentage = db.Column(db.Integer, default=0)
    last_accessed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    certificate_issued = db.Column(db.Boolean, default=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CourseEnrollment course_id={self.course_id} contact_id={self.contact_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'contact_id': self.contact_id,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'certificate_issued': self.certificate_issued,
            'enrolled_at': self.enrolled_at.isoformat() if self.enrolled_at else None
        }

