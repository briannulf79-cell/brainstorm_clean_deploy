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

# Import comprehensive models safely to avoid startup failures
try:
    from models.comprehensive_models import (
        Website, WebsiteTemplate, SubAccount, ContentPiece, SocialMediaAccount,
        MarketingFunnel, LandingPage, Survey, SurveyResponse, UnifiedCustomerProfile,
        Communication, Product, Order, AnalyticsEvent, Automation, AutomationExecution
    )
    COMPREHENSIVE_MODELS_AVAILABLE = True
    print("✅ Comprehensive business models loaded successfully")
except ImportError as e:
    print(f"⚠️  Warning: Comprehensive models not available: {e}")
    COMPREHENSIVE_MODELS_AVAILABLE = False
    # Create dummy classes to prevent NameError
    class Website: pass
    class WebsiteTemplate: pass
    class SubAccount: pass
    class ContentPiece: pass
    class MarketingFunnel: pass
    class Automation: pass

# Import business platform routes safely
try:
    from routes.business_platform import business_bp
    BUSINESS_ROUTES_AVAILABLE = True
    print("✅ Business platform routes loaded successfully")
except ImportError as e:
    print(f"⚠️  Warning: Business platform routes not available: {e}")
    BUSINESS_ROUTES_AVAILABLE = False

# Import subscription routes safely
try:
    from routes.subscription_routes import subscription_bp
    SUBSCRIPTION_ROUTES_AVAILABLE = True
    print("✅ Subscription routes loaded successfully")
except ImportError as e:
    print(f"⚠️  Warning: Subscription routes not available: {e}")
    SUBSCRIPTION_ROUTES_AVAILABLE = False

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

# Register business platform blueprint if available
if BUSINESS_ROUTES_AVAILABLE:
    app.register_blueprint(business_bp)
    print("✅ Business platform routes registered")
else:
    print("⚠️  Business platform routes not registered - using basic features only")

# Register subscription routes if available
if SUBSCRIPTION_ROUTES_AVAILABLE:
    app.register_blueprint(subscription_bp, url_prefix='/api/subscription')
    print("✅ Subscription routes registered")
else:
    print("⚠️  Subscription routes not registered - using basic subscription only")

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
        
        # Create sample website templates if comprehensive models available
        if COMPREHENSIVE_MODELS_AVAILABLE:
            try:
                templates = [
                    WebsiteTemplate(
                        name='Modern Business',
                        category='business',
                        description='Clean, professional template for businesses',
                        template_data={'theme': 'modern', 'colors': ['#007bff', '#ffffff']},
                        is_premium=False
                    ),
                    WebsiteTemplate(
                        name='E-commerce Pro',
                        category='ecommerce',
                        description='Full-featured online store template',
                        template_data={'theme': 'ecommerce', 'colors': ['#28a745', '#ffffff']},
                        is_premium=True
                    ),
                    WebsiteTemplate(
                        name='Creative Portfolio',
                        category='portfolio',
                        description='Showcase your work beautifully',
                        template_data={'theme': 'creative', 'colors': ['#6f42c1', '#ffffff']},
                        is_premium=False
                    )
                ]
                
                for template in templates:
                    db.session.add(template)
                
                print("Sample website templates created")
            except Exception as e:
                print(f"Warning: Could not create sample templates: {e}")
        
        db.session.commit()
        print("Master and Demo users created successfully.")

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

@app.route('/api/auth/demo', methods=['POST'])
def demo_login():
    """Demo login endpoint for quick access"""
    demo_user = User.query.filter_by(email='demo@brainstormaikit.com').first()
    
    if demo_user:
        access_token = create_access_token(identity=demo_user.id)
        return jsonify({
            'success': True, 
            'user': demo_user.to_dict(), 
            'token': access_token,
            'message': 'Welcome to the demo!'
        })
    else:
        return jsonify({'error': 'Demo account not found'}), 404

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    return jsonify({'user': request.current_user.to_dict()})

# Add simple health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Brainstorm AI Kit API is running',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/auth/reset-master-password', methods=['POST'])
def reset_master_password():
    """Reset master account password - for development/troubleshooting"""
    data = request.get_json()
    new_password = data.get('new_password', 'YourSecureMasterPassword123!')
    
    master_user = User.query.filter_by(email='brian.nulf79@gmail.com').first()
    if not master_user:
        # Create master user if it doesn't exist
        master_user = User(
            email='brian.nulf79@gmail.com',
            first_name='Brian',
            last_name='Nulf',
            password_hash=generate_password_hash(new_password),
            agency_name='Brainstorm AI Kit HQ',
            role='master'
        )
        db.session.add(master_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Master account created', 'password': new_password})
    else:
        master_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Master password reset', 'password': new_password})

@app.route('/api/dashboard', methods=['GET'])
@require_auth
def get_dashboard():
    """Comprehensive dashboard for the ultimate business platform"""
    try:
        user = request.current_user
        
        # Get user feature limits based on subscription tier
        feature_limits = user.get_feature_limits()
        
        # Determine user tier and capabilities
        if user.role == 'master':
            account_type = 'Master Account'
            subscription_status = 'Unlimited Access'
            tier = 'master'
        elif hasattr(user, 'subscription_tier') and user.subscription_tier == 'white_label':
            account_type = 'White Label Partner'
            subscription_status = 'White Label Active'
            tier = 'white_label'
        elif hasattr(user, 'subscription_tier'):
            account_type = f'{user.subscription_tier.replace("_", " ").title()} Plan'
            subscription_status = user.subscription_status.title() if hasattr(user, 'subscription_status') else 'Active'
            tier = user.subscription_tier
        else:
            account_type = 'Free Trial'
            subscription_status = 'Trial'
            tier = 'starter'
        
        # Build features_available for display
        features_available = feature_limits
        is_unlimited = user.role == 'master' or tier == 'white_label'
    
        # Get actual stats with fallbacks
        try:
            total_contacts = Contact.query.filter_by(sub_account_id=user.id).count()
        except:
            total_contacts = 0
        
        # Use sample data based on account type
        if user.role == 'master':
            sample_stats = {
                'total_contacts': max(total_contacts, 15234),
                'total_websites': 47,
                'total_funnels': 123,
                'total_content_pieces': 892,
                'active_automations': 34,
                'monthly_revenue': 89750
            }
        elif user.email == 'demo@brainstormaikit.com':
            sample_stats = {
                'total_contacts': max(total_contacts, 1247),
                'total_websites': 12,
                'total_funnels': 28,
                'total_content_pieces': 156,
                'active_automations': 18,
                'monthly_revenue': 12450
            }
        else:
            sample_stats = {
                'total_contacts': total_contacts,
                'total_websites': 0,
                'total_funnels': 0,
                'total_content_pieces': 0,
                'active_automations': 0,
                'monthly_revenue': 0
            }
        
        # Generate available features with proper limits
        available_features = [
            {
                'name': 'Website Builder',
                'description': f'Create {"unlimited" if is_unlimited else feature_limits.get("websites", 3)} professional websites',
                'icon': 'globe',
                'enabled': True,
                'limit': feature_limits.get('websites', 3)
            },
            {
                'name': 'AI Content Creator',
                'description': f'Generate {"unlimited" if is_unlimited else feature_limits.get("content_pieces_per_month", 50)} pieces/month',
                'icon': 'edit',
                'enabled': True,
                'limit': feature_limits.get('content_pieces_per_month', 50)
            },
            {
                'name': 'Marketing Funnels',
                'description': f'Build {"unlimited" if is_unlimited else feature_limits.get("funnels", 5)} high-converting funnels',
                'icon': 'trending-up',
                'enabled': True,
                'limit': feature_limits.get('funnels', 5)
            },
            {
                'name': 'CRM System',
                'description': f'Manage {"unlimited" if is_unlimited else f"{feature_limits.get("contacts", 1000):,}"} contacts',
                'icon': 'users',
                'enabled': True,
                'limit': feature_limits.get('contacts', 1000)
            },
            {
                'name': 'E-commerce Platform',
                'description': 'Sell products and services online',
                'icon': 'shopping-cart',
                'enabled': True,
                'limit': 'unlimited' if is_unlimited else 'basic'
            },
            {
                'name': 'Automation Hub',
                'description': f'Run {"unlimited" if is_unlimited else feature_limits.get("automations", 10)} workflows',
                'icon': 'zap',
                'enabled': True,
                'limit': feature_limits.get('automations', 10)
            },
            {
                'name': 'Analytics Suite',
                'description': 'Track and optimize performance',
                'icon': 'bar-chart',
                'enabled': True,
                'limit': 'advanced' if is_unlimited else 'basic'
            },
            {
                'name': 'Communication Hub',
                'description': f'{"Unlimited" if is_unlimited else f"{feature_limits.get("email_sends_per_month", 2000):,}"} emails/month',
                'icon': 'message-circle',
                'enabled': True
            },
            {
                'name': 'Survey & Forms',
                'description': 'Create and analyze customer feedback',
                'icon': 'clipboard',
                'enabled': True,
                'limit': feature_limits.get('email_sends_per_month', 2000)
            }
        ]
        
        # Add white-label features for appropriate tiers
        if feature_limits.get('white_label'):
            available_features.extend([
                {
                    'name': 'White-Label Solution',
                    'description': 'Complete rebrandable platform',
                    'icon': 'user-check',
                    'enabled': True,
                    'limit': 'unlimited'
                },
                {
                    'name': 'Sub-Account Management',
                    'description': 'Create unlimited client accounts',
                    'icon': 'clipboard',
                    'enabled': True,
                    'limit': feature_limits.get('sub_accounts', 'unlimited')
                }
            ])
        
        # Recent activity
        recent_activity = [
            {
                'description': f'Welcome to Brainstorm AI Kit, {user.first_name}!',
                'time': 'Just now',
                'type': 'welcome'
            },
            {
                'description': f'Your {account_type} is active and ready to use',
                'time': '1 minute ago',
                'type': 'system'
            }
        ]
        
        if user.role == 'master':
            recent_activity.append({
                'description': 'Master account privileges activated - unlimited access to all features',
                'time': '2 minutes ago',
                'type': 'success'
            })
        elif feature_limits.get('white_label'):
            recent_activity.append({
                'description': 'White-label features unlocked - start creating sub-accounts',
                'time': '2 minutes ago',
                'type': 'success'
            })
        
        # Get subscription plans for upgrade options
        subscription_plans = []
        try:
            from models.subscription_models import get_subscription_plans
            subscription_plans = get_subscription_plans()
        except ImportError:
            # Fallback subscription plans
            subscription_plans = [
                {
                    'tier': 'starter',
                    'name': 'Starter',
                    'monthly_price': 29,
                    'annual_price': 290,
                    'highlights': ['1,000 Contacts', '3 Websites', '50 AI Content/month']
                },
                {
                    'tier': 'professional',
                    'name': 'Professional',
                    'monthly_price': 99,
                    'annual_price': 990,
                    'highlights': ['10,000 Contacts', '25 Websites', '500 AI Content/month'],
                    'is_popular': True
                },
                {
                    'tier': 'white_label',
                    'name': 'White Label',
                    'monthly_price': 2999,
                    'annual_price': 29990,
                    'highlights': ['Unlimited Everything', 'White-Label Solution', 'Reseller Program']
                }
            ]
        
        # Build comprehensive dashboard data
        dashboard_data = {
            'user': user.to_dict(),
            'account_type': account_type,
            'subscription_status': subscription_status,
            'tier': tier,
            'features_available': features_available,
            'quick_stats': sample_stats,
            'recent_activity': recent_activity,
            'available_features': available_features,
            'subscription_info': {
                'tier': getattr(user, 'subscription_tier', 'starter'),
                'status': getattr(user, 'subscription_status', 'trial'),
                'days_remaining': user.days_remaining,
                'billing_cycle': getattr(user, 'billing_cycle', 'monthly'),
                'is_trial': getattr(user, 'subscription_status', 'trial') == 'trial',
                'is_master': user.role == 'master'
            },
            'subscription_plans': subscription_plans,
            'platform_stats': {
                'total_users': '50,000+',
                'websites_hosted': '125,000+',
                'ai_content_generated': '2.5M+',
                'customer_satisfaction': '98.7%'
            }
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return minimal working dashboard to prevent white screen
        try:
            user = request.current_user
            user_name = user.first_name if hasattr(user, 'first_name') else 'User'
            user_email = user.email if hasattr(user, 'email') else 'user@example.com'
            user_role = user.role if hasattr(user, 'role') else 'user'
        except:
            user_name = 'User'
            user_email = 'user@example.com'
            user_role = 'user'
        
        return jsonify({
            'user': {
                'first_name': user_name,
                'email': user_email,
                'role': user_role,
                'subscription_status': 'trial',
                'subscription_tier': 'starter'
            },
            'account_type': 'Master Account' if user_role == 'master' else 'Trial Account',
            'quick_stats': {
                'total_contacts': 0,
                'total_websites': 0,
                'total_funnels': 0,
                'total_content_pieces': 0,
                'active_automations': 0,
                'monthly_revenue': 0
            },
            'available_features': [
                {'name': 'Getting Started', 'description': 'Welcome to Brainstorm AI Kit!', 'icon': 'globe', 'enabled': True}
            ],
            'recent_activity': [
                {'description': 'Welcome to Brainstorm AI Kit!', 'time': 'Just now', 'type': 'welcome'}
            ],
            'error': 'Dashboard loading with basic functionality',
            'subscription_info': {
                'tier': 'starter',
                'status': 'trial',
                'days_remaining': 30,
                'is_master': user_role == 'master'
            }
        }), 200

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
