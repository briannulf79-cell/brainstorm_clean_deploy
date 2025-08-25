from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
import os
from database import get_db
from services.subscription_service import get_subscription_service
from models.subscription_models import SubscriptionTier

subscription_bp = Blueprint('subscription', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, os.getenv('SECRET_KEY', 'fallback-secret-key'), algorithms=['HS256'])
            current_user_id = data['user_id']
        except Exception as e:
            return jsonify({'message': 'Token is invalid', 'error': str(e)}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

@subscription_bp.route('/plans', methods=['GET'])
def get_subscription_plans():
    """Get all available subscription plans"""
    try:
        db = get_db()
        service = get_subscription_service(db)
        
        # Initialize plans if they don't exist
        service.initialize_default_plans()
        
        plans = service.get_all_plans()
        
        # Add plan benefits for frontend display
        for plan in plans:
            plan['highlights'] = get_plan_highlights(plan['tier'])
        
        return jsonify({
            'success': True,
            'plans': plans
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching plans: {str(e)}'
        }), 500

@subscription_bp.route('/current', methods=['GET'])
@token_required
def get_current_subscription(current_user_id):
    """Get user's current subscription details"""
    try:
        db = get_db()
        service = get_subscription_service(db)
        
        subscription = service.get_user_subscription(current_user_id)
        feature_summary = service.get_user_feature_summary(current_user_id)
        upgrade_recommendations = service.get_upgrade_recommendations(current_user_id)
        
        return jsonify({
            'success': True,
            'subscription': subscription,
            'feature_summary': feature_summary,
            'upgrade_recommendations': upgrade_recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching subscription: {str(e)}'
        }), 500

@subscription_bp.route('/upgrade', methods=['POST'])
@token_required
def upgrade_subscription(current_user_id):
    """Upgrade user subscription"""
    try:
        data = request.get_json()
        new_tier = data.get('tier')
        billing_cycle = data.get('billing_cycle', 'monthly')
        
        if not new_tier:
            return jsonify({
                'success': False,
                'message': 'Subscription tier is required'
            }), 400
        
        # Validate tier
        valid_tiers = [tier.value for tier in SubscriptionTier]
        if new_tier not in valid_tiers:
            return jsonify({
                'success': False,
                'message': 'Invalid subscription tier'
            }), 400
        
        db = get_db()
        service = get_subscription_service(db)
        
        # For now, directly upgrade (later integrate with Stripe)
        success = service.upgrade_subscription(current_user_id, new_tier, billing_cycle)
        
        if success:
            # Get updated subscription
            updated_subscription = service.get_user_subscription(current_user_id)
            
            return jsonify({
                'success': True,
                'message': 'Subscription upgraded successfully',
                'subscription': updated_subscription
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to upgrade subscription'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error upgrading subscription: {str(e)}'
        }), 500

@subscription_bp.route('/usage/<feature_name>', methods=['GET'])
@token_required
def get_feature_usage(current_user_id, feature_name):
    """Get usage information for a specific feature"""
    try:
        db = get_db()
        service = get_subscription_service(db)
        
        usage_info = service.check_feature_limit(current_user_id, feature_name)
        
        return jsonify({
            'success': True,
            'feature': feature_name,
            'usage': usage_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching usage: {str(e)}'
        }), 500

@subscription_bp.route('/usage/<feature_name>/increment', methods=['POST'])
@token_required
def increment_feature_usage(current_user_id, feature_name):
    """Increment usage for a feature (used when user performs actions)"""
    try:
        data = request.get_json()
        amount = data.get('amount', 1)
        
        db = get_db()
        service = get_subscription_service(db)
        
        # Check if user can use this feature
        usage_check = service.check_feature_limit(current_user_id, feature_name)
        if not usage_check.get('allowed', False):
            return jsonify({
                'success': False,
                'message': f'Feature limit exceeded for {feature_name}',
                'usage': usage_check
            }), 403
        
        # Increment usage
        success = service.increment_feature_usage(current_user_id, feature_name, amount)
        
        if success:
            # Get updated usage info
            updated_usage = service.check_feature_limit(current_user_id, feature_name)
            
            return jsonify({
                'success': True,
                'message': f'Usage incremented for {feature_name}',
                'usage': updated_usage
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to increment usage'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error incrementing usage: {str(e)}'
        }), 500

def get_plan_highlights(tier):
    """Get marketing highlights for each plan tier"""
    highlights = {
        SubscriptionTier.TRIAL.value: [
            "30-day free trial",
            "3 websites included",
            "100 contacts",
            "Basic AI content generation",
            "Email support"
        ],
        SubscriptionTier.STARTER.value: [
            "Perfect for small businesses",
            "10 websites & custom domain",
            "2,500 contacts",
            "10,000 monthly emails",
            "API access included"
        ],
        SubscriptionTier.PROFESSIONAL.value: [
            "Advanced business features", 
            "50 websites & priority support",
            "25,000 contacts",
            "Advanced analytics",
            "Remove branding"
        ],
        SubscriptionTier.ENTERPRISE.value: [
            "Large organization solution",
            "500 websites & dedicated support", 
            "100,000 contacts",
            "Custom integrations",
            "Custom development"
        ],
        SubscriptionTier.WHITE_LABEL.value: [
            "Ultimate reseller package",
            "Unlimited everything",
            "100 sub-accounts",
            "Revenue sharing",
            "White-label branding"
        ]
    }
    
    return highlights.get(tier, [])

# Export the blueprint
__all__ = ['subscription_bp']