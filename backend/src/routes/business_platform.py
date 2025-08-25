"""
Comprehensive Business Platform API Routes
All the endpoints for the ultimate business platform features
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Contact
from models.comprehensive_models import *
from services.openai_service import openai_service
from services.stripe_service import stripe_service
from datetime import datetime
import uuid

# Create blueprint for business platform routes
business_bp = Blueprint('business', __name__)

# Helper function to get current user
def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)

# Website Builder & Hosting
@business_bp.route('/api/websites', methods=['GET'])
@jwt_required()
def get_websites():
    user = get_current_user()
    websites = Website.query.filter_by(user_id=user.id).all()
    return jsonify({
        'websites': [website.to_dict() for website in websites],
        'total': len(websites),
        'limit': 'unlimited' if user.role == 'master' else '10'
    })

@business_bp.route('/api/websites', methods=['POST'])
@jwt_required()
def create_website():
    user = get_current_user()
    data = request.get_json()
    
    # Generate unique subdomain
    subdomain = data.get('subdomain') or f"{data['title'].lower().replace(' ', '-')}-{uuid.uuid4().hex[:8]}"
    
    website = Website(
        user_id=user.id,
        subdomain=subdomain,
        custom_domain=data.get('custom_domain'),
        title=data['title'],
        description=data.get('description', ''),
        template_id=data.get('template_id', 'default'),
        content=data.get('content', {}),
        seo_settings=data.get('seo_settings', {}),
        is_published=data.get('is_published', False)
    )
    
    db.session.add(website)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'website': website.to_dict(),
        'live_url': f"https://{subdomain}.brainstormaikit.com"
    })

@business_bp.route('/api/website-templates', methods=['GET'])
@jwt_required()
def get_website_templates():
    templates = WebsiteTemplate.query.all()
    return jsonify({
        'templates': [template.to_dict() for template in templates]
    })

# Sub-Account Management (White Label)
@business_bp.route('/api/sub-accounts', methods=['GET'])
@jwt_required()
def get_sub_accounts():
    user = get_current_user()
    sub_accounts = SubAccount.query.filter_by(parent_user_id=user.id).all()
    return jsonify({
        'sub_accounts': [account.to_dict() for account in sub_accounts]
    })

@business_bp.route('/api/sub-accounts', methods=['POST'])
@jwt_required()
def create_sub_account():
    user = get_current_user()
    data = request.get_json()
    
    # Generate subdomain
    subdomain = f"{data['business_name'].lower().replace(' ', '-')}-{user.id}"
    
    sub_account = SubAccount(
        parent_user_id=user.id,
        business_name=data['business_name'],
        subdomain=subdomain,
        custom_branding=data.get('custom_branding', {}),
        permissions=data.get('permissions', {}),
        billing_settings=data.get('billing_settings', {})
    )
    
    db.session.add(sub_account)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'sub_account': sub_account.to_dict(),
        'access_url': f"https://{subdomain}.brainstormaikit.com"
    })

# Content Creation & Management
@business_bp.route('/api/content', methods=['GET'])
@jwt_required()
def get_content():
    user = get_current_user()
    content_type = request.args.get('type', 'all')
    
    query = ContentPiece.query.filter_by(user_id=user.id)
    if content_type != 'all':
        query = query.filter_by(content_type=content_type)
    
    content_pieces = query.order_by(ContentPiece.created_at.desc()).all()
    
    return jsonify({
        'content': [piece.to_dict() for piece in content_pieces],
        'types': ['blog_post', 'social_media', 'video_script', 'email', 'ad_copy', 'press_release']
    })

@business_bp.route('/api/content/generate', methods=['POST'])
@jwt_required()
def generate_content():
    user = get_current_user()
    data = request.get_json()
    
    # Use OpenAI to generate content
    ai_prompt = data['prompt']
    content_type = data['content_type']
    
    # Generate content using AI
    generated_content = openai_service.generate_content(
        content_type=content_type,
        prompt=ai_prompt,
        tone=data.get('tone', 'professional'),
        length=data.get('length', 'medium')
    )
    
    content_piece = ContentPiece(
        user_id=user.id,
        title=data.get('title', f"AI Generated {content_type.title()}"),
        content_type=content_type,
        content=generated_content,
        ai_generated=True,
        ai_prompt=ai_prompt,
        target_platforms=data.get('target_platforms', []),
        status='draft'
    )
    
    db.session.add(content_piece)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'content': content_piece.to_dict()
    })

@business_bp.route('/api/content/<int:content_id>/publish', methods=['POST'])
@jwt_required()
def publish_content(content_id):
    user = get_current_user()
    content_piece = ContentPiece.query.filter_by(id=content_id, user_id=user.id).first()
    
    if not content_piece:
        return jsonify({'error': 'Content not found'}), 404
    
    data = request.get_json()
    platforms = data.get('platforms', [])
    
    # Publish to selected platforms
    results = {}
    for platform in platforms:
        # Here you would integrate with each platform's API
        # For now, we'll simulate the publishing
        results[platform] = {'status': 'scheduled', 'post_id': f"{platform}_{uuid.uuid4().hex[:8]}"}
    
    content_piece.status = 'published'
    db.session.commit()
    
    return jsonify({
        'success': True,
        'publishing_results': results
    })

# Social Media Management
@business_bp.route('/api/social-accounts', methods=['GET'])
@jwt_required()
def get_social_accounts():
    user = get_current_user()
    accounts = SocialMediaAccount.query.filter_by(user_id=user.id).all()
    return jsonify({
        'accounts': [account.to_dict() for account in accounts],
        'supported_platforms': ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok']
    })

@business_bp.route('/api/social-accounts', methods=['POST'])
@jwt_required()
def connect_social_account():
    user = get_current_user()
    data = request.get_json()
    
    account = SocialMediaAccount(
        user_id=user.id,
        platform=data['platform'],
        account_name=data['account_name'],
        access_token=data['access_token'],  # This would be encrypted in production
        account_id=data['account_id'],
        is_connected=True
    )
    
    db.session.add(account)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'account': account.to_dict()
    })

# Marketing Funnels & Landing Pages
@business_bp.route('/api/funnels', methods=['GET'])
@jwt_required()
def get_funnels():
    user = get_current_user()
    funnels = MarketingFunnel.query.filter_by(user_id=user.id).all()
    return jsonify({
        'funnels': [funnel.to_dict() for funnel in funnels]
    })

@business_bp.route('/api/funnels/generate', methods=['POST'])
@jwt_required()
def generate_funnel():
    user = get_current_user()
    data = request.get_json()
    
    # AI-generate funnel structure
    funnel_config = openai_service.generate_marketing_funnel(
        business_type=data['business_type'],
        target_audience=data['target_audience'],
        goal=data['goal']
    )
    
    funnel = MarketingFunnel(
        user_id=user.id,
        name=data['name'],
        description=data.get('description', ''),
        funnel_type=data['funnel_type'],
        steps=funnel_config['steps'],
        conversion_tracking=funnel_config['tracking']
    )
    
    db.session.add(funnel)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'funnel': funnel.to_dict()
    })

@business_bp.route('/api/landing-pages', methods=['GET'])
@jwt_required()
def get_landing_pages():
    user = get_current_user()
    pages = LandingPage.query.filter_by(user_id=user.id).all()
    return jsonify({
        'landing_pages': [page.to_dict() for page in pages]
    })

@business_bp.route('/api/landing-pages', methods=['POST'])
@jwt_required()
def create_landing_page():
    user = get_current_user()
    data = request.get_json()
    
    # Generate unique slug
    slug = data.get('slug') or f"{data['name'].lower().replace(' ', '-')}-{uuid.uuid4().hex[:8]}"
    
    page = LandingPage(
        user_id=user.id,
        funnel_id=data.get('funnel_id'),
        name=data['name'],
        slug=slug,
        template_id=data.get('template_id', 'default'),
        content=data.get('content', {}),
        seo_settings=data.get('seo_settings', {}),
        conversion_elements=data.get('conversion_elements', {})
    )
    
    db.session.add(page)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'landing_page': page.to_dict(),
        'live_url': f"https://{user.id}.brainstormaikit.com/p/{slug}"
    })

# Surveys & Forms
@business_bp.route('/api/surveys', methods=['GET'])
@jwt_required()
def get_surveys():
    user = get_current_user()
    surveys = Survey.query.filter_by(user_id=user.id).all()
    return jsonify({
        'surveys': [survey.to_dict() for survey in surveys]
    })

@business_bp.route('/api/surveys', methods=['POST'])
@jwt_required()
def create_survey():
    user = get_current_user()
    data = request.get_json()
    
    survey = Survey(
        user_id=user.id,
        title=data['title'],
        description=data.get('description', ''),
        questions=data['questions'],
        settings=data.get('settings', {})
    )
    
    db.session.add(survey)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'survey': survey.to_dict()
    })

# Enhanced CRM
@business_bp.route('/api/customer-profiles', methods=['GET'])
@jwt_required()
def get_customer_profiles():
    user = get_current_user()
    profiles = UnifiedCustomerProfile.query.filter_by(user_id=user.id).all()
    return jsonify({
        'profiles': [profile.to_dict() for profile in profiles]
    })

@business_bp.route('/api/customer-profiles/<int:contact_id>', methods=['GET'])
@jwt_required()
def get_customer_profile(contact_id):
    user = get_current_user()
    profile = UnifiedCustomerProfile.query.filter_by(
        user_id=user.id, 
        contact_id=contact_id
    ).first()
    
    if not profile:
        # Create profile if it doesn't exist
        contact = Contact.query.filter_by(id=contact_id, sub_account_id=user.id).first()
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404
            
        profile = UnifiedCustomerProfile(
            user_id=user.id,
            contact_id=contact_id,
            interaction_history=[],
            behavioral_data={},
            engagement_score=50.0
        )
        db.session.add(profile)
        db.session.commit()
    
    return jsonify({
        'profile': profile.to_dict()
    })

# E-commerce
@business_bp.route('/api/products', methods=['GET'])
@jwt_required()
def get_products():
    user = get_current_user()
    products = Product.query.filter_by(user_id=user.id).all()
    return jsonify({
        'products': [product.to_dict() for product in products]
    })

@business_bp.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    user = get_current_user()
    data = request.get_json()
    
    product = Product(
        user_id=user.id,
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        currency=data.get('currency', 'USD'),
        sku=data.get('sku'),
        inventory_count=data.get('inventory_count', 0),
        digital_product=data.get('digital_product', False),
        download_url=data.get('download_url'),
        images=data.get('images', []),
        categories=data.get('categories', [])
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'product': product.to_dict()
    })

@business_bp.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user = get_current_user()
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return jsonify({
        'orders': [order.to_dict() for order in orders]
    })

# Analytics & Reporting
@business_bp.route('/api/analytics/dashboard', methods=['GET'])
@jwt_required()
def get_analytics_dashboard():
    user = get_current_user()
    
    # Comprehensive analytics data
    total_contacts = Contact.query.filter_by(sub_account_id=user.id).count()
    total_websites = Website.query.filter_by(user_id=user.id).count()
    total_funnels = MarketingFunnel.query.filter_by(user_id=user.id).count()
    total_orders = Order.query.filter_by(user_id=user.id).count()
    
    # Recent activity
    recent_events = AnalyticsEvent.query.filter_by(user_id=user.id)\
        .order_by(AnalyticsEvent.created_at.desc()).limit(50).all()
    
    return jsonify({
        'overview': {
            'total_contacts': total_contacts,
            'total_websites': total_websites,
            'total_funnels': total_funnels,
            'total_orders': total_orders,
            'conversion_rate': 3.2,  # Calculate from actual data
            'revenue_this_month': 15420.50  # Calculate from actual data
        },
        'recent_activity': [event.to_dict() for event in recent_events]
    })

# Communication Hub
@business_bp.route('/api/communications', methods=['GET'])
@jwt_required()
def get_communications():
    user = get_current_user()
    channel = request.args.get('channel', 'all')
    
    query = Communication.query.filter_by(user_id=user.id)
    if channel != 'all':
        query = query.filter_by(channel=channel)
    
    communications = query.order_by(Communication.created_at.desc()).limit(100).all()
    
    return jsonify({
        'communications': [comm.to_dict() for comm in communications]
    })

# Automation & Workflows
@business_bp.route('/api/automations', methods=['GET'])
@jwt_required()
def get_automations():
    user = get_current_user()
    automations = Automation.query.filter_by(user_id=user.id).all()
    return jsonify({
        'automations': [automation.to_dict() for automation in automations]
    })

@business_bp.route('/api/automations', methods=['POST'])
@jwt_required()
def create_automation():
    user = get_current_user()
    data = request.get_json()
    
    automation = Automation(
        user_id=user.id,
        name=data['name'],
        description=data.get('description', ''),
        trigger_type=data['trigger_type'],
        trigger_conditions=data.get('trigger_conditions', {}),
        workflow_steps=data['workflow_steps']
    )
    
    db.session.add(automation)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'automation': automation.to_dict()
    })