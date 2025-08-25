import os
import stripe
from datetime import datetime, timedelta
from models import db, User, Subscription
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StripeService:
    def __init__(self):
        self.api_key = os.environ.get('STRIPE_SECRET_KEY')
        self.webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
        
        if not self.api_key:
            logger.warning("Stripe API key not configured. Payment functionality will be disabled.")
            self.enabled = False
        else:
            stripe.api_key = self.api_key
            self.enabled = True

    def create_checkout_session(self, user_id, plan_name='Pro Plan', plan_price=97.00):
        """Create a Stripe checkout session for subscription"""
        if not self.enabled:
            logger.warning("Stripe service disabled")
            return None

        try:
            user = User.query.get(user_id)
            if not user:
                return None

            # Create checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': plan_name,
                            'description': 'AI-Powered CRM & Marketing Automation Platform'
                        },
                        'unit_amount': int(plan_price * 100),  # Convert to cents
                        'recurring': {
                            'interval': 'month'
                        }
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{os.getenv('FRONTEND_URL', 'https://app.brainstormaikit.com')}/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{os.getenv('FRONTEND_URL', 'https://app.brainstormaikit.com')}/upgrade",
                customer_email=user.email,
                metadata={
                    'user_id': str(user_id),
                    'plan_name': plan_name
                }
            )
            
            return session
            
        except Exception as e:
            logger.error(f"Error creating Stripe checkout session: {str(e)}")
            return None

    def handle_webhook(self, payload, sig_header):
        """Handle Stripe webhook events"""
        if not self.enabled or not self.webhook_secret:
            return False

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            
            # Handle successful subscription creation
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                self._handle_successful_payment(session)
                
            # Handle subscription updates
            elif event['type'] == 'invoice.payment_succeeded':
                invoice = event['data']['object']
                self._handle_subscription_renewal(invoice)
                
            # Handle failed payments
            elif event['type'] == 'invoice.payment_failed':
                invoice = event['data']['object']
                self._handle_failed_payment(invoice)
                
            return True
            
        except Exception as e:
            logger.error(f"Error handling Stripe webhook: {str(e)}")
            return False

    def _handle_successful_payment(self, session):
        """Handle successful subscription payment"""
        try:
            user_id = session.get('metadata', {}).get('user_id')
            if not user_id:
                return

            user = User.query.get(int(user_id))
            if not user:
                return

            # Update user subscription status
            user.subscription_status = 'active'
            user.subscription_expires_at = datetime.utcnow() + timedelta(days=30)
            
            # Create subscription record
            subscription = Subscription(
                user_id=user.id,
                plan_name=session.get('metadata', {}).get('plan_name', 'Pro Plan'),
                plan_price=97.00,
                status='active',
                stripe_subscription_id=session.get('subscription'),
                current_period_start=datetime.utcnow(),
                current_period_end=datetime.utcnow() + timedelta(days=30)
            )
            
            db.session.add(subscription)
            db.session.commit()
            
            logger.info(f"Successfully activated subscription for user {user.email}")
            
        except Exception as e:
            logger.error(f"Error handling successful payment: {str(e)}")

    def _handle_subscription_renewal(self, invoice):
        """Handle subscription renewal"""
        try:
            subscription_id = invoice['subscription']
            stripe_subscription = stripe.Subscription.retrieve(subscription_id)
            
            # Find user by Stripe customer
            customer_email = stripe.Customer.retrieve(invoice['customer'])['email']
            user = User.query.filter_by(email=customer_email).first()
            
            if user:
                user.subscription_expires_at = datetime.fromtimestamp(
                    stripe_subscription['current_period_end']
                )
                db.session.commit()
                logger.info(f"Renewed subscription for user {user.email}")
                
        except Exception as e:
            logger.error(f"Error handling subscription renewal: {str(e)}")

    def _handle_failed_payment(self, invoice):
        """Handle failed payment"""
        try:
            customer_email = stripe.Customer.retrieve(invoice['customer'])['email']
            user = User.query.filter_by(email=customer_email).first()
            
            if user:
                # Could send email notification about failed payment
                logger.warning(f"Payment failed for user {user.email}")
                
        except Exception as e:
            logger.error(f"Error handling failed payment: {str(e)}")

# Global instance
stripe_service = StripeService()