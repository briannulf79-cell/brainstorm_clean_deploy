from flask import Blueprint, request, jsonify
from src.models.user import db, User, UserSession
from src.models.agency import Agency, SubAccount
from datetime import datetime, timedelta
import hashlib
import secrets

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Create session token
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        session = UserSession(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        db.session.add(session)
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'token': token,
            'user': user.to_dict(),
            'expires_at': expires_at.isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        agency_name = data.get('agency_name')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User with this email already exists'}), 400
        
        # Create agency if provided
        agency = None
        if agency_name:
            agency = Agency(name=agency_name, plan_type='starter')
            db.session.add(agency)
            db.session.flush()  # Get the agency ID
        
        # Create user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='admin' if agency else 'user',
            agency_id=agency.id if agency else None
        )
        user.set_password(password)
        db.session.add(user)
        
        # Create default sub-account if agency was created
        if agency:
            sub_account = SubAccount(
                agency_id=agency.id,
                name=f"{agency_name} - Main",
                industry='general'
            )
            db.session.add(sub_account)
        
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        session = UserSession.query.filter_by(token_hash=token_hash).first()
        
        if not session or session.expires_at < datetime.utcnow():
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = User.query.get(session.user_id)
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        return jsonify({'user': user.to_dict()})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if token:
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            session = UserSession.query.filter_by(token_hash=token_hash).first()
            if session:
                db.session.delete(session)
                db.session.commit()
        
        return jsonify({'message': 'Logged out successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

