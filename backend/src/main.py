import os
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from models import db, User, Contact, Subscription
from services.notification_service import notification_service
from services.stripe_service import stripe_service
from services.twilio_service import twilio_service
from services.openai_service import openai_service
from services.demo_service import demo_service

# --- App Initialization ---
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# --- Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///brainstorm_ai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'a-super-secret-key-for-dev')

# Handle PostgreSQL URL format for Railway
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

# --- Initialize Extensions ---
db.init_app(app)
jwt = JWTManager(app)

# --- Database Initialization and Seeding ---
with app.app_context():
    db.create_all()

    # Seed the database ONLY if it's completely empty
    if User.query.count() == 0:
        print("Database is empty. Seeding with demo data...")
        
        # MASTER ACCOUNT: This is your free, permanent master account.
        master_user = User(
            email='brian.nulf79@gmail.com', # Use your actual email here
            first_name='Brian',
            last_name='Nulf',
            password_hash=generate_password_hash('YourSecureMasterPassword123!'), # CHOOSE A STRONG, UNIQUE PASSWORD
            agency_name='Brainstorm AI Kit HQ',
            role='master'  # The special role that grants permanent access
        )
        
        # Demo user for showcasing the product
        demo_user = User(
            email='demo@brainstormaikit.com',
            first_name='Demo',
            last_name='User',
            password_hash=generate_password_hash('demo123'),
            agency_name='Demo Agency',
            role='user'
        )
        
        db.session.add(master_user)
        db.session.add(demo_user)
        db.session.commit()
        print("Master and Demo users created.")

# --- Authentication Logic with Master Account Check ---

# This is the function that protects your API routes
def require_auth(f):
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # MASTER ACCOUNT CHECK: If the user's role is 'master', bypass all subscription checks.
        if user.role == 'master':
            request.current_user = user
            return f(*args, **kwargs)

        # For regular users, check the trial/subscription status
        if user.is_subscription_active:
            request.current_user = user
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Subscription required. Please upgrade your plan.', 'subscription_required': True}), 403
            
    decorated_function.__name__ = f.__name__
    return decorated_function

# --- API Endpoints ---

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

# Authentication
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(
        email=data['email'],
        first_name=data['firstName'],
        last_name=data['lastName'],
        password_hash=generate_password_hash(data['password']),
        agency_name=data.get('agencyName', ''),
        role='user' # All new signups are regular 'user' roles
    )
    db.session.add(user)
    db.session.commit()
    
    # Send welcome email
    notification_service.send_welcome_email_to_new_user(user)
    
    # Ensure clean account for new users (except demo)
    demo_service.clean_user_account(user)
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'success': True,
        'user': user.to_dict(),
        'token': access_token,
        'message': f'Welcome! Your 30-day trial has started.'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        # For master and active users, grant access
        if user.role == 'master' or user.is_subscription_active:
            access_token = create_access_token(identity=user.id)
            return jsonify({'success': True, 'user': user.to_dict(), 'token': access_token})
        else: # Handle expired regular users
            return jsonify({'error': 'Your trial has expired or your subscription is inactive.', 'subscription_required': True}), 403
    
    return jsonify({'error': 'Invalid credentials'}), 401

# All other endpoints (contacts, dashboard, etc.) will use @require_auth
# and automatically work with the master account logic.

@app.route('/api/contacts', methods=['GET'])
@require_auth
def get_contacts():
    # Get contacts based on user type (demo vs regular users)
    contacts = demo_service.get_user_contacts(request.current_user)
    return jsonify({'contacts': [contact.to_dict() for contact in contacts]})

@app.route('/api/contacts', methods=['POST'])
@require_auth
def create_contact():
    data = request.get_json()
    
    # Create contact with provided data
    contact = Contact(
        sub_account_id=request.current_user.id,  # Link to current user
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone', ''),
        company=data.get('company', ''),
        source=data.get('source', 'manual'),
        notes=data.get('notes', '')
    )
    
    # Generate AI lead score
    contact_data = {
        'email': contact.email,
        'company': contact.company,
        'phone': contact.phone,
        'source': contact.source,
        'notes': contact.notes
    }
    contact.lead_score = openai_service.generate_lead_score(contact_data)
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify({'success': True, 'contact': contact.to_dict()}), 201

# Trial and notification management
@app.route('/api/admin/check-trial-notifications', methods=['POST'])
@require_auth
def check_trial_notifications():
    # Only allow master users to trigger notifications
    if request.current_user.role != 'master':
        return jsonify({'error': 'Unauthorized - Admin access required'}), 403
    
    notification_service.check_and_send_trial_notifications()
    return jsonify({'success': True, 'message': 'Trial notifications checked and sent'})

@app.route('/api/user/upgrade-subscription', methods=['POST'])
@require_auth
def upgrade_subscription():
    """Create Stripe checkout session for subscription upgrade"""
    data = request.get_json()
    user = request.current_user
    
    plan_name = data.get('plan_name', 'Pro Plan')
    plan_price = data.get('plan_price', 97.00)
    
    session = stripe_service.create_checkout_session(
        user_id=user.id,
        plan_name=plan_name,
        plan_price=plan_price
    )
    
    if session:
        return jsonify({
            'success': True,
            'checkout_url': session.url,
            'session_id': session.id
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to create checkout session'
        }), 500

@app.route('/api/stripe/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    if stripe_service.handle_webhook(payload, sig_header):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Webhook processing failed'}), 400

# AI-powered features
@app.route('/api/ai/lead-score', methods=['POST'])
@require_auth
def calculate_lead_score():
    """Calculate AI lead score for contact data"""
    data = request.get_json()
    score = openai_service.generate_lead_score(data)
    return jsonify({'lead_score': score})

@app.route('/api/ai/email-content', methods=['POST'])
@require_auth
def generate_email_content():
    """Generate AI email content"""
    data = request.get_json()
    content = openai_service.generate_email_content(
        purpose=data.get('purpose', 'follow-up'),
        contact_name=data.get('contact_name'),
        company_name=data.get('company_name'),
        additional_context=data.get('additional_context')
    )
    return jsonify(content)

@app.route('/api/ai/follow-up-suggestions', methods=['POST'])
@require_auth
def get_follow_up_suggestions():
    """Get AI follow-up suggestions for a contact"""
    data = request.get_json()
    suggestions = openai_service.suggest_follow_up_actions(
        contact_data=data.get('contact_data', {}),
        interaction_history=data.get('interaction_history')
    )
    return jsonify({'suggestions': suggestions})

# Communication features  
@app.route('/api/sms/send', methods=['POST'])
@require_auth
def send_sms():
    """Send SMS to contact"""
    data = request.get_json()
    
    success = twilio_service.send_sms(
        to_number=data['phone_number'],
        message=data['message']
    )
    
    if success:
        return jsonify({'success': True, 'message': 'SMS sent successfully'})
    else:
        return jsonify({'success': False, 'error': 'Failed to send SMS'}), 500

# Service status endpoints for admin
@app.route('/api/admin/service-status', methods=['GET'])
@require_auth
def get_service_status():
    """Get status of all integrated services (admin only)"""
    if request.current_user.role != 'master':
        return jsonify({'error': 'Unauthorized - Admin access required'}), 403
    
    status = {
        'email_service': email_service.enabled,
        'stripe_service': stripe_service.enabled,
        'twilio_service': twilio_service.enabled,
        'openai_service': openai_service.enabled
    }
    
    # Test connections
    if openai_service.enabled:
        status['openai_test'] = openai_service.test_connection()
    
    if twilio_service.enabled:
        status['twilio_account'] = twilio_service.get_account_info()
    
    return jsonify(status)

@app.route('/api/user/account-status', methods=['GET'])
@require_auth
def get_account_status():
    """Get detailed account status including trial information"""
    user = request.current_user
    
    status_info = {
        'user': user.to_dict(),
        'trial_info': {
            'is_trial': user.subscription_status == 'trial',
            'is_expired': user.is_trial_expired,
            'days_remaining': user.days_remaining,
            'expires_at': user.trial_expires_at.isoformat() if user.trial_expires_at else None
        },
        'subscription_required': not user.is_subscription_active and user.role != 'master'
    }
    
    return jsonify(status_info)

# --- Main Execution Block ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
