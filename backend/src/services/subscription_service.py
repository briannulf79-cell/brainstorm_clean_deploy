import os
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from models.subscription_models import (
    SubscriptionPlan, UserSubscription, FeatureUsage, 
    SubscriptionTier, SUBSCRIPTION_FEATURES,
    get_user_feature_limit, check_feature_access, is_feature_unlimited
)

class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db
    
    def initialize_default_plans(self):
        """Initialize default subscription plans if they don't exist"""
        try:
            existing_plans = self.db.query(SubscriptionPlan).count()
            if existing_plans > 0:
                return
            
            default_plans = [
                {
                    'name': 'Free Trial',
                    'tier': SubscriptionTier.TRIAL.value,
                    'price_monthly': Decimal('0.00'),
                    'price_yearly': Decimal('0.00'),
                    'description': 'Perfect for getting started - explore all features with generous limits for 30 days',
                    'features': SUBSCRIPTION_FEATURES[SubscriptionTier.TRIAL]
                },
                {
                    'name': 'Starter Plan',
                    'tier': SubscriptionTier.STARTER.value,
                    'price_monthly': Decimal('29.99'),
                    'price_yearly': Decimal('299.99'),
                    'description': 'Ideal for small businesses and entrepreneurs ready to scale their operations',
                    'features': SUBSCRIPTION_FEATURES[SubscriptionTier.STARTER]
                },
                {
                    'name': 'Professional Plan',
                    'tier': SubscriptionTier.PROFESSIONAL.value,
                    'price_monthly': Decimal('99.99'),
                    'price_yearly': Decimal('999.99'),
                    'description': 'Perfect for growing businesses that need advanced features and higher limits',
                    'features': SUBSCRIPTION_FEATURES[SubscriptionTier.PROFESSIONAL]
                },
                {
                    'name': 'Enterprise Plan',
                    'tier': SubscriptionTier.ENTERPRISE.value,
                    'price_monthly': Decimal('299.99'),
                    'price_yearly': Decimal('2999.99'),
                    'description': 'Comprehensive solution for large organizations with extensive business needs',
                    'features': SUBSCRIPTION_FEATURES[SubscriptionTier.ENTERPRISE]
                },
                {
                    'name': 'White Label Ultimate',
                    'tier': SubscriptionTier.WHITE_LABEL.value,
                    'price_monthly': Decimal('999.99'),
                    'price_yearly': Decimal('9999.99'),
                    'description': 'The ultimate reseller package - unlimited everything with white-label capabilities and revenue sharing',
                    'features': SUBSCRIPTION_FEATURES[SubscriptionTier.WHITE_LABEL]
                }
            ]
            
            for plan_data in default_plans:
                plan = SubscriptionPlan(**plan_data)
                self.db.add(plan)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error initializing subscription plans: {e}")
            return False
    
    def get_all_plans(self) -> List[Dict]:
        """Get all active subscription plans"""
        try:
            plans = self.db.query(SubscriptionPlan).filter(SubscriptionPlan.is_active == True).all()
            return [plan.to_dict() for plan in plans]
        except Exception as e:
            print(f"Error getting subscription plans: {e}")
            return []
    
    def get_plan_by_tier(self, tier: str) -> Optional[Dict]:
        """Get subscription plan by tier"""
        try:
            plan = self.db.query(SubscriptionPlan).filter(
                SubscriptionPlan.tier == tier,
                SubscriptionPlan.is_active == True
            ).first()
            return plan.to_dict() if plan else None
        except Exception as e:
            print(f"Error getting plan by tier: {e}")
            return None
    
    def get_user_subscription(self, user_id: int) -> Optional[Dict]:
        """Get user's current subscription"""
        try:
            subscription = self.db.query(UserSubscription).filter(
                UserSubscription.user_id == user_id,
                UserSubscription.status.in_(['active', 'trial'])
            ).first()
            return subscription.to_dict() if subscription else None
        except Exception as e:
            print(f"Error getting user subscription: {e}")
            return None
    
    def create_trial_subscription(self, user_id: int) -> bool:
        """Create a trial subscription for new user"""
        try:
            # Check if user already has a subscription
            existing = self.db.query(UserSubscription).filter(
                UserSubscription.user_id == user_id
            ).first()
            
            if existing:
                return True  # Already has subscription
            
            # Get trial plan
            trial_plan = self.db.query(SubscriptionPlan).filter(
                SubscriptionPlan.tier == SubscriptionTier.TRIAL.value
            ).first()
            
            if not trial_plan:
                return False
            
            # Create trial subscription
            trial_end = datetime.utcnow() + timedelta(days=30)
            subscription = UserSubscription(
                user_id=user_id,
                plan_id=trial_plan.id,
                status='trial',
                current_period_start=datetime.utcnow(),
                current_period_end=trial_end
            )
            
            self.db.add(subscription)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error creating trial subscription: {e}")
            return False
    
    def upgrade_subscription(self, user_id: int, new_tier: str, billing_cycle: str = 'monthly') -> bool:
        """Upgrade user subscription to new tier"""
        try:
            # Get new plan
            new_plan = self.db.query(SubscriptionPlan).filter(
                SubscriptionPlan.tier == new_tier,
                SubscriptionPlan.is_active == True
            ).first()
            
            if not new_plan:
                return False
            
            # Get current subscription
            current_subscription = self.db.query(UserSubscription).filter(
                UserSubscription.user_id == user_id,
                UserSubscription.status.in_(['active', 'trial'])
            ).first()
            
            if current_subscription:
                # Update existing subscription
                current_subscription.plan_id = new_plan.id
                current_subscription.status = 'active'
                current_subscription.billing_cycle = billing_cycle
                current_subscription.current_period_start = datetime.utcnow()
                
                # Set new period end based on billing cycle
                if billing_cycle == 'yearly':
                    current_subscription.current_period_end = datetime.utcnow() + timedelta(days=365)
                else:
                    current_subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
                
                current_subscription.updated_at = datetime.utcnow()
            else:
                # Create new subscription
                period_end = datetime.utcnow() + timedelta(days=365 if billing_cycle == 'yearly' else 30)
                subscription = UserSubscription(
                    user_id=user_id,
                    plan_id=new_plan.id,
                    status='active',
                    billing_cycle=billing_cycle,
                    current_period_start=datetime.utcnow(),
                    current_period_end=period_end
                )
                self.db.add(subscription)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error upgrading subscription: {e}")
            return False
    
    def check_feature_limit(self, user_id: int, feature_name: str) -> Dict[str, Any]:
        """Check if user can use a feature based on their limits"""
        try:
            # Get user subscription
            subscription = self.get_user_subscription(user_id)
            if not subscription:
                tier = SubscriptionTier.TRIAL.value
            else:
                tier = subscription['plan']['tier']
            
            # Check if feature is unlimited
            if is_feature_unlimited(tier, feature_name):
                return {
                    'allowed': True,
                    'unlimited': True,
                    'usage_count': 0,
                    'limit': 'unlimited'
                }
            
            # Get feature limit
            limit = get_user_feature_limit(tier, feature_name)
            if limit is False or limit == 0:
                return {
                    'allowed': False,
                    'unlimited': False,
                    'usage_count': 0,
                    'limit': 0
                }
            
            # Get current usage
            usage = self.db.query(FeatureUsage).filter(
                FeatureUsage.user_id == user_id,
                FeatureUsage.feature_name == feature_name
            ).first()
            
            if not usage:
                # Create usage record
                usage = FeatureUsage(
                    user_id=user_id,
                    feature_name=feature_name,
                    usage_count=0,
                    usage_limit=limit
                )
                self.db.add(usage)
                self.db.commit()
            
            return {
                'allowed': usage.usage_count < limit,
                'unlimited': False,
                'usage_count': usage.usage_count,
                'limit': limit,
                'percentage_used': (usage.usage_count / limit * 100) if limit > 0 else 0
            }
        except Exception as e:
            print(f"Error checking feature limit: {e}")
            return {'allowed': False, 'error': str(e)}
    
    def increment_feature_usage(self, user_id: int, feature_name: str, amount: int = 1) -> bool:
        """Increment feature usage for user"""
        try:
            usage = self.db.query(FeatureUsage).filter(
                FeatureUsage.user_id == user_id,
                FeatureUsage.feature_name == feature_name
            ).first()
            
            if usage:
                usage.usage_count += amount
                usage.updated_at = datetime.utcnow()
            else:
                # Get user tier to set limit
                subscription = self.get_user_subscription(user_id)
                tier = subscription['plan']['tier'] if subscription else SubscriptionTier.TRIAL.value
                limit = get_user_feature_limit(tier, feature_name)
                
                usage = FeatureUsage(
                    user_id=user_id,
                    feature_name=feature_name,
                    usage_count=amount,
                    usage_limit=limit if limit != 'unlimited' else None
                )
                self.db.add(usage)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error incrementing feature usage: {e}")
            return False
    
    def get_user_feature_summary(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive feature summary for user"""
        try:
            subscription = self.get_user_subscription(user_id)
            if not subscription:
                tier = SubscriptionTier.TRIAL.value
                features = SUBSCRIPTION_FEATURES[SubscriptionTier.TRIAL]
            else:
                tier = subscription['plan']['tier']
                features = subscription['plan']['features']
            
            # Get all feature usage for user
            usage_records = self.db.query(FeatureUsage).filter(
                FeatureUsage.user_id == user_id
            ).all()
            
            usage_dict = {usage.feature_name: usage.to_dict() for usage in usage_records}
            
            feature_summary = {}
            for feature_name, limit in features.items():
                usage_data = usage_dict.get(feature_name, {
                    'usage_count': 0,
                    'usage_limit': limit if limit != 'unlimited' else None,
                    'percentage_used': 0
                })
                
                feature_summary[feature_name] = {
                    'limit': limit,
                    'unlimited': limit == 'unlimited',
                    'usage_count': usage_data.get('usage_count', 0),
                    'percentage_used': usage_data.get('percentage_used', 0),
                    'available': limit == 'unlimited' or usage_data.get('usage_count', 0) < limit if limit not in [False, 0] else False
                }
            
            return {
                'subscription': subscription,
                'tier': tier,
                'features': feature_summary
            }
        except Exception as e:
            print(f"Error getting user feature summary: {e}")
            return {}
    
    def get_upgrade_recommendations(self, user_id: int) -> List[Dict]:
        """Get upgrade recommendations based on usage patterns"""
        try:
            feature_summary = self.get_user_feature_summary(user_id)
            current_tier = feature_summary.get('tier')
            
            if not current_tier:
                return []
            
            # Find features that are close to limits or exceeded
            upgrade_triggers = []
            for feature_name, data in feature_summary.get('features', {}).items():
                if not data['unlimited'] and data['limit'] not in [False, 0]:
                    usage_percentage = data['percentage_used']
                    if usage_percentage > 80:
                        upgrade_triggers.append({
                            'feature': feature_name,
                            'usage_percentage': usage_percentage,
                            'reason': f"You're using {usage_percentage:.1f}% of your {feature_name.replace('_', ' ')} limit"
                        })
            
            # Get available upgrade options
            all_plans = self.get_all_plans()
            current_plan_index = None
            
            tier_order = [
                SubscriptionTier.TRIAL.value,
                SubscriptionTier.STARTER.value,
                SubscriptionTier.PROFESSIONAL.value,
                SubscriptionTier.ENTERPRISE.value,
                SubscriptionTier.WHITE_LABEL.value
            ]
            
            try:
                current_plan_index = tier_order.index(current_tier)
            except ValueError:
                current_plan_index = 0
            
            upgrade_options = []
            for i in range(current_plan_index + 1, len(tier_order)):
                tier = tier_order[i]
                plan = next((p for p in all_plans if p['tier'] == tier), None)
                if plan:
                    upgrade_options.append(plan)
            
            return {
                'upgrade_triggers': upgrade_triggers,
                'recommended_plans': upgrade_options,
                'should_upgrade': len(upgrade_triggers) > 0
            }
        except Exception as e:
            print(f"Error getting upgrade recommendations: {e}")
            return {'upgrade_triggers': [], 'recommended_plans': [], 'should_upgrade': False}

def get_subscription_service(db: Session) -> SubscriptionService:
    """Get subscription service instance"""
    return SubscriptionService(db)