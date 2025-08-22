import os
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from models import db, User, Contact, Subscription

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
    # This is now protected. Only logged-in, active (or master) users can access it.
    contacts = Contact.query.filter_by(sub_account_id=1).all()
    return jsonify({'contacts': [contact.to_dict() for contact in contacts]})

@app.route('/api/contacts', methods=['POST'])
@require_auth
def create_contact():
    data = request.get_json()
    contact = Contact(
        sub_account_id=data.get('sub_account_id', 1),
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify({'success': True, 'contact': contact.to_dict()}), 201

# --- Main Execution Block ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
