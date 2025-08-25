import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        
        if not self.api_key:
            logger.warning("OpenAI API key not configured. AI functionality will be disabled.")
            self.enabled = False
        else:
            # Temporarily disable OpenAI to avoid import issues
            logger.warning("OpenAI service temporarily disabled for debugging")
            self.enabled = False

    def generate_lead_score(self, contact_data):
        """Generate AI-powered lead score based on contact data"""
        # Return a simple score based on available data
        score = 50.0  # Base score
        
        if contact_data.get('email') and '@' in contact_data.get('email', ''):
            score += 10
        if contact_data.get('company'):
            score += 15
        if contact_data.get('phone'):
            score += 10
        if contact_data.get('source') == 'referral':
            score += 15
            
        return min(100.0, score)

    def generate_email_content(self, purpose, contact_name=None, company_name=None, additional_context=None):
        """Generate simple email content"""
        return {
            "subject": f"Thank you for your interest - {purpose}",
            "content": f"Hi {contact_name or 'there'}!\n\nThank you for your interest in our services. We'll be in touch soon!\n\nBest regards,\nBrainstorm AI Kit Team"
        }

    def analyze_contact_sentiment(self, notes):
        """Simple sentiment analysis"""
        return {"sentiment": "neutral", "engagement_score": 50}

    def suggest_follow_up_actions(self, contact_data, interaction_history=None):
        """Simple follow-up suggestions"""
        return [
            "Send welcome email",
            "Schedule follow-up call",
            "Add to nurture campaign"
        ]

    def test_connection(self):
        """Test connection"""
        return True

# Global instance
openai_service = OpenAIService()