import os
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from models import db, User, Contact, Subscription

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'brainstorm_ai_kit_secret_key_2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///brainstorm_ai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Handle PostgreSQL URL format for Railway
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

# Initialize extensions
db.init_app(app)
CORS(app, origins="*")

# Create tables
with app.app_context():
    db.create_all()
    
    # Create demo users if they don't exist
    if not User.query.filter_by(email='demo@brainstormaikit.com').first():
        demo_user = User(
            email='demo@brainstormaikit.com',
            first_name='Demo',
            last_name='User',
            password_hash=generate_password_hash('demo123'),
            agency_name='Demo Agency',
            role='user'
        )
        db.session.add(demo_user)
    
    if not User.query.filter_by(email='admin@brainstormaikit.com').first():
        admin_user = User(
            email='admin@brainstormaikit.com',
            first_name='Admin',
            last_name='User',
            password_hash=generate_password_hash('demo123'),
            agency_name='Brainstorm AI Kit',
            role='admin'
        )
        db.session.add(admin_user)
    
    # Add some demo contacts
    if Contact.query.count() == 0:
        demo_contacts = [
            Contact(
                first_name='Sarah',
                last_name='Johnson',
                email='sarah.johnson@example.com',
                phone='+1-555-0123',
                company='Tech Solutions Inc',
                source='website',
                tags='["hot-lead", "enterprise"]',
                lead_score=85.5
            ),
            Contact(
                first_name='Michael',
                last_name='Chen',
                email='michael.chen@example.com',
                phone='+1-555-0124',
                company='Digital Marketing Pro',
                source='referral',
                tags='["warm-lead", "smb"]',
                lead_score=72.3
            ),
            Contact(
                first_name='Emily',
                last_name='Rodriguez',
                email='emily.rodriguez@example.com',
                phone='+1-555-0125',
                company='Growth Agency LLC',
                source='social_media',
                tags='["cold-lead", "agency"]',
                lead_score=91.2
            )
        ]
        for contact in demo_contacts:
            db.session.add(contact)
    
    db.session.commit()

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            token = token.replace('Bearer ', '')
            user_id = verify_token(token)
            if user_id:
                user = User.query.get(user_id)
                if user and user.is_subscription_active:
                    request.current_user = user
                    return f(*args, **kwargs)
                elif user and user.is_trial_expired:
                    return jsonify({'error': 'Trial expired. Please upgrade to continue.', 'trial_expired': True}), 403
        return jsonify({'error': 'Authentication required'}), 401
    decorated_function.__name__ = f.__name__
    return decorated_function

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'service': 'Brainstorm AI Kit API', 'version': '1.0.0'}

# Authentication endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user with 30-day trial
    user = User(
        email=data['email'],
        first_name=data['firstName'],
        last_name=data['lastName'],
        password_hash=generate_password_hash(data['password']),
        agency_name=data.get('agencyName', ''),
        role='user'
    )
    
    db.session.add(user)
    db.session.commit()
    
    token = generate_token(user.id)
    
    return jsonify({
        'success': True,
        'user': user.to_dict(),
        'token': token,
        'message': f'Welcome! Your 30-day trial has started. You have {user.days_remaining} days remaining.'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        if user.is_subscription_active:
            token = generate_token(user.id)
            return jsonify({
                'success': True,
                'user': user.to_dict(),
                'token': token
            })
        else:
            return jsonify({
                'error': 'Your trial has expired. Please upgrade to continue.',
                'trial_expired': True,
                'user': user.to_dict()
            }), 403
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Dashboard endpoints
@app.route('/api/dashboard/overview', methods=['GET'])
@require_auth
def dashboard_overview():
    user = request.current_user
    total_contacts = Contact.query.filter_by(sub_account_id=1).count()
    
    return jsonify({
        'total_contacts': total_contacts,
        'new_contacts_this_month': 12,  # Could be calculated from created_at
        'total_revenue': 125000,
        'revenue_growth': 12.5,
        'active_campaigns': 8,
        'conversion_rate': 3.2,
        'user_info': user.to_dict()
    })

# Contact endpoints
@app.route('/api/contacts', methods=['GET'])
@require_auth
def get_contacts():
    sub_account_id = request.args.get('sub_account_id', 1)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = Contact.query.filter_by(sub_account_id=sub_account_id)
    
    if search:
        query = query.filter(
            (Contact.first_name.contains(search)) |
            (Contact.last_name.contains(search)) |
            (Contact.email.contains(search)) |
            (Contact.company.contains(search))
        )
    
    if status and status != 'all':
        query = query.filter_by(status=status)
    
    contacts = query.order_by(Contact.created_at.desc()).all()
    
    return jsonify({
        'contacts': [contact.to_dict() for contact in contacts],
        'total': len(contacts)
    })

@app.route('/api/contacts', methods=['POST'])
@require_auth
def create_contact():
    data = request.get_json()
    
    # Convert tags list to JSON string
    tags_json = json.dumps(data.get('tags', []))
    
    contact = Contact(
        sub_account_id=data.get('sub_account_id', 1),
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone', ''),
        company=data.get('company', ''),
        source=data.get('source', ''),
        tags=tags_json,
        notes=data.get('notes', ''),
        lead_score=data.get('lead_score', 50.0)  # Default score
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'contact': contact.to_dict(),
        'message': 'Contact created successfully'
    }), 201

# Subscription endpoints
@app.route('/api/subscription/status', methods=['GET'])
@require_auth
def subscription_status():
    user = request.current_user
    return jsonify(user.to_dict())

@app.route('/api/subscription/upgrade', methods=['POST'])
@require_auth
def upgrade_subscription():
    data = request.get_json()
    user = request.current_user
    
    # In a real app, this would integrate with Stripe
    # For now, we'll simulate the upgrade
    plan_name = data.get('plan', 'professional')
    billing_cycle = data.get('billing_cycle', 'monthly')
    
    # Update user subscription
    user.subscription_status = 'active'
    user.subscription_expires_at = datetime.utcnow() + timedelta(days=365 if billing_cycle == 'yearly' else 30)
    
    # Create subscription record
    subscription = Subscription(
        user_id=user.id,
        plan_name=plan_name,
        plan_price=297 if plan_name == 'professional' else 97,  # Example pricing
        billing_cycle=billing_cycle,
        current_period_start=datetime.utcnow(),
        current_period_end=user.subscription_expires_at
    )
    
    db.session.add(subscription)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Subscription upgraded successfully!',
        'user': user.to_dict(),
        'subscription': subscription.to_dict()
    })

# Analytics endpoints
@app.route('/api/analytics/overview', methods=['GET'])
@require_auth
def analytics_overview():
    total_contacts = Contact.query.count()
    
    return jsonify({
        'total_contacts': total_contacts,
        'new_contacts': 12,
        'total_revenue': 125000,
        'revenue_growth': 12.5,
        'conversion_rate': 3.2,
        'conversion_change': 0.8,
        'avg_deal_size': 4500,
        'deal_size_change': -2.1
    })

# AI insights endpoints
@app.route('/api/ai/insights', methods=['GET'])
@require_auth
def ai_insights():
    return jsonify({
        'insights': [
            {
                'type': 'performance',
                'title': 'Strong Performance Detected',
                'description': 'Your conversion rate is 23% above industry average.',
                'confidence': 87,
                'impact': 'positive'
            },
            {
                'type': 'opportunity',
                'title': 'Lead Scoring Optimization',
                'description': 'AI suggests focusing on contacts with scores above 80.',
                'confidence': 73,
                'impact': 'neutral'
            }
        ]
    })

@app.route('/')
def home():
    return {'message': 'Brainstorm AI Kit API is running!', 'version': '1.0.0'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

