import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            logger.warning("Twilio credentials not fully configured. SMS functionality will be disabled.")
            self.enabled = False
        else:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.enabled = True
                logger.info("Twilio service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {str(e)}")
                self.enabled = False

    def send_sms(self, to_number, message):
        """Send SMS message using Twilio"""
        if not self.enabled:
            logger.warning(f"Twilio service disabled. Would have sent SMS to {to_number}: {message}")
            return False

        try:
            # Ensure phone number is in E.164 format
            if not to_number.startswith('+'):
                to_number = '+1' + to_number.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')

            message = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            
            logger.info(f"SMS sent successfully to {to_number}. SID: {message.sid}")
            return True
            
        except TwilioException as e:
            logger.error(f"Twilio error sending SMS to {to_number}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"General error sending SMS to {to_number}: {str(e)}")
            return False

    def send_welcome_sms(self, to_number, first_name):
        """Send welcome SMS to new users"""
        message = f"Hi {first_name}! Welcome to Brainstorm AI Kit 🧠 Your 30-day free trial is now active! Login to start building: https://app.brainstormaikit.com"
        return self.send_sms(to_number, message)

    def send_trial_warning_sms(self, to_number, first_name, days_remaining):
        """Send trial expiration warning SMS"""
        if days_remaining == 7:
            message = f"Hi {first_name}! Your Brainstorm AI Kit trial expires in 7 days. Don't lose your data - upgrade now: https://app.brainstormaikit.com/upgrade"
        elif days_remaining == 1:
            message = f"URGENT: Hi {first_name}! Your trial expires TOMORROW. Upgrade now to keep your account active: https://app.brainstormaikit.com/upgrade"
        else:
            message = f"Hi {first_name}! Your Brainstorm AI Kit trial expires in {days_remaining} days. Upgrade: https://app.brainstormaikit.com/upgrade"
        
        return self.send_sms(to_number, message)

    def send_marketing_sms(self, to_number, campaign_message):
        """Send marketing SMS campaign"""
        return self.send_sms(to_number, campaign_message)

    def validate_phone_number(self, phone_number):
        """Validate phone number using Twilio Lookup API"""
        if not self.enabled:
            return False

        try:
            from twilio.rest import Client
            lookup_client = Client(self.account_sid, self.auth_token)
            
            phone_number_obj = lookup_client.lookups.phone_numbers(phone_number).fetch()
            return phone_number_obj.phone_number is not None
            
        except Exception as e:
            logger.error(f"Error validating phone number {phone_number}: {str(e)}")
            return False

    def get_account_info(self):
        """Get Twilio account information for admin/debugging"""
        if not self.enabled:
            return None

        try:
            account = self.client.api.accounts(self.account_sid).fetch()
            return {
                'account_sid': account.sid,
                'friendly_name': account.friendly_name,
                'status': account.status,
                'type': account.type
            }
        except Exception as e:
            logger.error(f"Error fetching Twilio account info: {str(e)}")
            return None

# Global instance
twilio_service = TwilioService()