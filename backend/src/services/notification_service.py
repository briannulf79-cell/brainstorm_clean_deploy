import os
from datetime import datetime, timedelta
from services.email_service import email_service
from models import db, User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    """Service to handle trial notifications and lifecycle management"""
    
    def check_and_send_trial_notifications(self):
        """Check all users and send appropriate trial notifications"""
        try:
            # Find users who need 7-day warnings
            seven_days_from_now = datetime.utcnow() + timedelta(days=7)
            users_7_day_warning = User.query.filter(
                User.subscription_status == 'trial',
                User.role != 'master',
                User.trial_expires_at.between(
                    seven_days_from_now - timedelta(hours=12),
                    seven_days_from_now + timedelta(hours=12)
                )
            ).all()
            
            for user in users_7_day_warning:
                logger.info(f"Sending 7-day trial warning to {user.email}")
                email_service.send_trial_warning_email(
                    user.email, 
                    user.first_name, 
                    7
                )
            
            # Find users who need 1-day warnings
            one_day_from_now = datetime.utcnow() + timedelta(days=1)
            users_1_day_warning = User.query.filter(
                User.subscription_status == 'trial',
                User.role != 'master',
                User.trial_expires_at.between(
                    one_day_from_now - timedelta(hours=12),
                    one_day_from_now + timedelta(hours=12)
                )
            ).all()
            
            for user in users_1_day_warning:
                logger.info(f"Sending 1-day trial warning to {user.email}")
                email_service.send_trial_warning_email(
                    user.email, 
                    user.first_name, 
                    1
                )
            
            # Find users whose trials just expired
            recently_expired = User.query.filter(
                User.subscription_status == 'trial',
                User.role != 'master',
                User.trial_expires_at.between(
                    datetime.utcnow() - timedelta(hours=24),
                    datetime.utcnow()
                )
            ).all()
            
            for user in recently_expired:
                logger.info(f"Sending trial expired notification to {user.email}")
                email_service.send_trial_expired_email(
                    user.email, 
                    user.first_name
                )
                # Update user status to expired
                user.subscription_status = 'expired'
                db.session.commit()
                
        except Exception as e:
            logger.error(f"Error in trial notification check: {str(e)}")
            
    def send_welcome_email_to_new_user(self, user):
        """Send welcome email to newly registered user"""
        try:
            logger.info(f"Sending welcome email to {user.email}")
            return email_service.send_welcome_email(
                user.email,
                user.first_name
            )
        except Exception as e:
            logger.error(f"Error sending welcome email to {user.email}: {str(e)}")
            return False

# Global instance
notification_service = NotificationService()