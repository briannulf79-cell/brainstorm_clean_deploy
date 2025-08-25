"""
Comprehensive Subscription System Models
Multi-tier subscription plans with white-label capabilities
"""
from datetime import datetime, timedelta
from models import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Decimal, JSON, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

class SubscriptionTier(Enum):
    STARTER = 'starter'
    PROFESSIONAL = 'professional'
    BUSINESS = 'business'
    ENTERPRISE = 'enterprise'
    WHITE_LABEL = 'white_label'

class BillingCycle(Enum):
    MONTHLY = 'monthly'
    ANNUALLY = 'annually'

class SubscriptionPlan(db.Model):
    """Subscription plan details and pricing"""
    __tablename__ = 'subscription_plans'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)  # 'Starter', 'Professional', etc.
    tier = Column(String(20), nullable=False)  # 'starter', 'professional', etc.
    description = Column(Text)
    tagline = Column(String(255))  # Short marketing tagline
    monthly_price = Column(Decimal(10, 2), nullable=False)
    annual_price = Column(Decimal(10, 2), nullable=False)
    setup_fee = Column(Decimal(10, 2), default=0)
    features = Column(JSON, nullable=False)  # Feature limits as JSON
    feature_highlights = Column(JSON)  # Key features to highlight in UI
    stripe_monthly_price_id = Column(String(100))
    stripe_annual_price_id = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)  # Mark as "Most Popular"
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def get_annual_savings(self):
        """Calculate annual savings amount"""
        monthly_total = float(self.monthly_price * 12)
        annual_total = float(self.annual_price)
        return max(0, monthly_total - annual_total)
    
    def get_annual_savings_percent(self):
        """Calculate annual savings percentage"""
        monthly_total = float(self.monthly_price * 12)
        savings = self.get_annual_savings()
        return round((savings / monthly_total) * 100) if monthly_total > 0 else 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tier': self.tier,
            'description': self.description,
            'tagline': self.tagline,
            'monthly_price': float(self.monthly_price),
            'annual_price': float(self.annual_price),
            'setup_fee': float(self.setup_fee),
            'annual_savings': self.get_annual_savings(),
            'annual_savings_percent': self.get_annual_savings_percent(),
            'features': self.features,
            'feature_highlights': self.feature_highlights,
            'stripe_monthly_price_id': self.stripe_monthly_price_id,
            'stripe_annual_price_id': self.stripe_annual_price_id,
            'is_active': self.is_active,
            'is_popular': self.is_popular,
            'sort_order': self.sort_order
        }

class UsageTracking(db.Model):
    """Track monthly usage for billing and limits"""
    __tablename__ = 'usage_tracking'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    month = Column(String(7), nullable=False)  # Format: 'YYYY-MM'
    usage_data = Column(JSON, nullable=False)  # Track various usage metrics
    overage_charges = Column(Decimal(10, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('User', backref='usage_history')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'month': self.month,
            'usage_data': self.usage_data,
            'overage_charges': float(self.overage_charges),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class WhiteLabelBranding(db.Model):
    """White-label branding settings for reseller accounts"""
    __tablename__ = 'white_label_branding'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company_name = Column(String(100), nullable=False)
    logo_url = Column(String(500))
    primary_color = Column(String(7), default='#3B82F6')
    secondary_color = Column(String(7), default='#1E40AF')
    accent_color = Column(String(7), default='#10B981')
    custom_domain = Column(String(255))
    favicon_url = Column(String(500))
    
    # Email branding
    email_from_name = Column(String(100))
    email_from_address = Column(String(120))
    email_footer = Column(Text)
    
    # Support contact info
    support_email = Column(String(120))
    support_phone = Column(String(20))
    
    # Legal pages
    terms_url = Column(String(500))
    privacy_url = Column(String(500))
    
    # Custom styling
    footer_text = Column(Text)
    custom_css = Column(Text)
    
    # Reseller settings
    reseller_commission_rate = Column(Decimal(5, 2), default=30.00)  # 30% commission
    allow_sub_resellers = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('User', backref='white_label_branding')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_name': self.company_name,
            'logo_url': self.logo_url,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'accent_color': self.accent_color,
            'custom_domain': self.custom_domain,
            'favicon_url': self.favicon_url,
            'email_from_name': self.email_from_name,
            'email_from_address': self.email_from_address,
            'email_footer': self.email_footer,
            'support_email': self.support_email,
            'support_phone': self.support_phone,
            'terms_url': self.terms_url,
            'privacy_url': self.privacy_url,
            'footer_text': self.footer_text,
            'custom_css': self.custom_css,
            'reseller_commission_rate': float(self.reseller_commission_rate),
            'allow_sub_resellers': self.allow_sub_resellers,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Define comprehensive feature limits and pricing
SUBSCRIPTION_FEATURES = {
    'starter': {
        'name': 'Starter',
        'tagline': 'Perfect for small businesses getting started',
        'monthly_price': 29,
        'annual_price': 290,  # 2 months free
        'features': {
            'contacts': 1000,
            'websites': 3,
            'funnels': 5,
            'content_pieces_per_month': 50,
            'automations': 10,
            'email_sends_per_month': 2000,
            'sms_sends_per_month': 100,
            'storage_gb': 5,
            'team_members': 2,
            'white_label': False,
            'sub_accounts': 0,
            'api_calls_per_month': 1000,
            'custom_domain': False,
            'priority_support': False,
            'phone_support': False,
            'integrations': ['basic'],
            'analytics_retention_days': 90
        },
        'highlights': [
            '1,000 Contacts',
            '3 Websites',
            '5 Marketing Funnels',
            '50 AI Content Pieces/month',
            '2,000 Email Sends/month',
            'Basic Analytics',
            'Email Support'
        ]
    },
    'professional': {
        'name': 'Professional',
        'tagline': 'Ideal for growing businesses and agencies',
        'monthly_price': 99,
        'annual_price': 990,  # 2 months free
        'features': {
            'contacts': 10000,
            'websites': 25,
            'funnels': 50,
            'content_pieces_per_month': 500,
            'automations': 100,
            'email_sends_per_month': 20000,
            'sms_sends_per_month': 1000,
            'storage_gb': 50,
            'team_members': 10,
            'white_label': False,
            'sub_accounts': 0,
            'api_calls_per_month': 10000,
            'custom_domain': True,
            'priority_support': True,
            'phone_support': False,
            'integrations': ['basic', 'premium'],
            'analytics_retention_days': 365,
            'a_b_testing': True,
            'advanced_automations': True
        },
        'highlights': [
            '10,000 Contacts',
            '25 Websites',
            '50 Marketing Funnels',
            '500 AI Content Pieces/month',
            '20,000 Email Sends/month',
            'Custom Domain',
            'A/B Testing',
            'Priority Support'
        ]
    },
    'business': {
        'name': 'Business',
        'tagline': 'For established businesses scaling operations',
        'monthly_price': 299,
        'annual_price': 2990,  # 2 months free
        'features': {
            'contacts': 100000,
            'websites': 100,
            'funnels': 200,
            'content_pieces_per_month': 2000,
            'automations': 500,
            'email_sends_per_month': 100000,
            'sms_sends_per_month': 5000,
            'storage_gb': 200,
            'team_members': 50,
            'white_label': False,
            'sub_accounts': 0,
            'api_calls_per_month': 50000,
            'custom_domain': True,
            'priority_support': True,
            'phone_support': True,
            'integrations': ['basic', 'premium', 'enterprise'],
            'analytics_retention_days': 1095,  # 3 years
            'a_b_testing': True,
            'advanced_automations': True,
            'multi_language': True,
            'advanced_reporting': True
        },
        'highlights': [
            '100,000 Contacts',
            '100 Websites',
            '200 Marketing Funnels',
            '2,000 AI Content Pieces/month',
            '100,000 Email Sends/month',
            'Multi-language Support',
            'Advanced Reporting',
            'Phone Support'
        ]
    },
    'enterprise': {
        'name': 'Enterprise',
        'tagline': 'Complete solution for large organizations',
        'monthly_price': 999,
        'annual_price': 9990,  # 2 months free
        'features': {
            'contacts': 1000000,
            'websites': 500,
            'funnels': 1000,
            'content_pieces_per_month': 10000,
            'automations': 2000,
            'email_sends_per_month': 1000000,
            'sms_sends_per_month': 25000,
            'storage_gb': 1000,
            'team_members': 200,
            'white_label': False,
            'sub_accounts': 0,
            'api_calls_per_month': 500000,
            'custom_domain': True,
            'priority_support': True,
            'phone_support': True,
            'integrations': ['basic', 'premium', 'enterprise', 'custom'],
            'analytics_retention_days': 2555,  # 7 years
            'a_b_testing': True,
            'advanced_automations': True,
            'multi_language': True,
            'advanced_reporting': True,
            'dedicated_account_manager': True,
            'custom_integrations': True,
            'sso': True,
            'audit_logs': True
        },
        'highlights': [
            '1,000,000 Contacts',
            '500 Websites',
            '1,000 Marketing Funnels',
            '10,000 AI Content Pieces/month',
            '1,000,000 Email Sends/month',
            'Dedicated Account Manager',
            'Custom Integrations',
            'SSO & Audit Logs'
        ]
    },
    'white_label': {
        'name': 'White Label',
        'tagline': 'Complete reseller solution with unlimited capabilities',
        'monthly_price': 2999,
        'annual_price': 29990,  # 2 months free
        'features': {
            'contacts': 'unlimited',
            'websites': 'unlimited',
            'funnels': 'unlimited',
            'content_pieces_per_month': 'unlimited',
            'automations': 'unlimited',
            'email_sends_per_month': 'unlimited',
            'sms_sends_per_month': 'unlimited',
            'storage_gb': 'unlimited',
            'team_members': 'unlimited',
            'white_label': True,
            'sub_accounts': 'unlimited',
            'api_calls_per_month': 'unlimited',
            'custom_domain': True,
            'priority_support': True,
            'phone_support': True,
            'integrations': ['basic', 'premium', 'enterprise', 'custom'],
            'analytics_retention_days': 'unlimited',
            'a_b_testing': True,
            'advanced_automations': True,
            'multi_language': True,
            'advanced_reporting': True,
            'dedicated_account_manager': True,
            'custom_integrations': True,
            'sso': True,
            'audit_logs': True,
            'reseller_program': True,
            'custom_branding': True,
            'revenue_sharing': True,
            'white_label_mobile_app': True
        },
        'highlights': [
            'Unlimited Everything',
            'Complete White-Label Solution',
            'Unlimited Sub-Accounts',
            'Revenue Sharing Program',
            'Custom Branding',
            'Reseller Dashboard',
            'White-Label Mobile App',
            'Priority Implementation'
        ]
    }
}

def get_user_feature_limits(user_tier, user_role='user'):
    """Get feature limits for a user based on their subscription tier"""
    if user_role == 'master':
        return SUBSCRIPTION_FEATURES['white_label']['features']
    
    return SUBSCRIPTION_FEATURES.get(user_tier, SUBSCRIPTION_FEATURES['starter'])['features']

def get_subscription_plans():
    """Get all available subscription plans"""
    plans = []
    for tier, data in SUBSCRIPTION_FEATURES.items():
        plans.append({
            'tier': tier,
            'name': data['name'],
            'tagline': data['tagline'],
            'monthly_price': data['monthly_price'],
            'annual_price': data['annual_price'],
            'annual_savings': (data['monthly_price'] * 12) - data['annual_price'],
            'annual_savings_percent': round(((data['monthly_price'] * 12) - data['annual_price']) / (data['monthly_price'] * 12) * 100),
            'features': data['features'],
            'highlights': data['highlights'],
            'is_popular': tier == 'professional',  # Mark Professional as popular
            'sort_order': ['starter', 'professional', 'business', 'enterprise', 'white_label'].index(tier)
        })
    
    return sorted(plans, key=lambda x: x['sort_order'])