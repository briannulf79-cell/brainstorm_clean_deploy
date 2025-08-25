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
            try:
                # Import OpenAI only when needed to avoid version conflicts
                import openai
                openai.api_key = self.api_key
                self.enabled = True
                logger.info("OpenAI service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                self.enabled = False

    def generate_lead_score(self, contact_data):
        """Generate AI-powered lead score based on contact data"""
        if not self.enabled:
            logger.warning("OpenAI service disabled. Returning default lead score.")
            return 50.0  # Default score

        try:
            prompt = f"""
            Based on the following contact information, provide a lead score from 0-100 where:
            - 0-30: Low quality lead
            - 31-70: Medium quality lead  
            - 71-100: High quality lead
            
            Contact Data:
            - Email: {contact_data.get('email', 'N/A')}
            - Company: {contact_data.get('company', 'N/A')}
            - Phone: {contact_data.get('phone', 'N/A')}
            - Source: {contact_data.get('source', 'N/A')}
            - Notes: {contact_data.get('notes', 'N/A')}
            
            Consider factors like:
            - Professional email domain vs personal email
            - Company presence and size indicators
            - Contact completeness
            - Source quality
            
            Respond with just a number between 0-100.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI lead scoring assistant that provides accurate numerical lead scores."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.3
            )
            
            score_text = response.choices[0].message.content.strip()
            try:
                score = float(score_text)
                return max(0.0, min(100.0, score))  # Ensure score is between 0-100
            except ValueError:
                logger.warning(f"Invalid score format from OpenAI: {score_text}")
                return 50.0
                
        except Exception as e:
            logger.error(f"Error generating lead score: {str(e)}")
            return 50.0

    def generate_email_content(self, purpose, contact_name=None, company_name=None, additional_context=None):
        """Generate AI-powered email content for marketing campaigns"""
        if not self.enabled:
            return {"subject": "Default Subject", "content": "Default email content"}

        try:
            context = f"Contact Name: {contact_name or 'Valued Customer'}\n"
            if company_name:
                context += f"Company: {company_name}\n"
            if additional_context:
                context += f"Additional Context: {additional_context}\n"

            prompt = f"""
            Generate a professional email for the following purpose: {purpose}
            
            Context:
            {context}
            
            Requirements:
            - Professional and engaging tone
            - Clear call-to-action
            - Personalized when possible
            - Appropriate length (not too long)
            - Include subject line
            
            Respond in JSON format with "subject" and "content" fields.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert email marketing copywriter who creates engaging, professional emails."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                lines = content.split('\n')
                subject = lines[0].replace('Subject:', '').strip() if lines else 'AI Generated Email'
                email_content = '\n'.join(lines[1:]).strip() if len(lines) > 1 else content
                return {"subject": subject, "content": email_content}
                
        except Exception as e:
            logger.error(f"Error generating email content: {str(e)}")
            return {
                "subject": "Personalized Message for You",
                "content": f"Hi {contact_name or 'there'}!\n\nWe wanted to reach out regarding {purpose}.\n\nBest regards,\nThe Brainstorm AI Kit Team"
            }

    def analyze_contact_sentiment(self, notes):
        """Analyze sentiment and engagement level from contact notes"""
        if not self.enabled or not notes:
            return {"sentiment": "neutral", "engagement_score": 50}

        try:
            prompt = f"""
            Analyze the sentiment and engagement level of these contact notes:
            
            "{notes}"
            
            Provide:
            1. Sentiment: positive, negative, or neutral
            2. Engagement score: 0-100 (0=not engaged, 100=highly engaged)
            
            Respond in JSON format with "sentiment" and "engagement_score" fields.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI sentiment analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"sentiment": "neutral", "engagement_score": 50}
                
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {"sentiment": "neutral", "engagement_score": 50}

    def suggest_follow_up_actions(self, contact_data, interaction_history=None):
        """Suggest AI-powered follow-up actions for contacts"""
        if not self.enabled:
            return ["Send follow-up email", "Schedule phone call", "Add to nurture campaign"]

        try:
            context = f"""
            Contact: {contact_data.get('first_name', '')} {contact_data.get('last_name', '')}
            Company: {contact_data.get('company', 'N/A')}
            Lead Score: {contact_data.get('lead_score', 'N/A')}
            Status: {contact_data.get('status', 'N/A')}
            Source: {contact_data.get('source', 'N/A')}
            Notes: {contact_data.get('notes', 'N/A')}
            """
            
            if interaction_history:
                context += f"\nRecent Interactions: {interaction_history}"

            prompt = f"""
            Based on this contact information, suggest 3-5 specific follow-up actions:
            
            {context}
            
            Suggestions should be:
            - Actionable and specific
            - Appropriate for the contact's status and engagement
            - Business-focused
            
            Respond as a JSON array of strings.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a CRM assistant that provides actionable follow-up recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.6
            )
            
            suggestions = response.choices[0].message.content.strip()
            try:
                return json.loads(suggestions)
            except json.JSONDecodeError:
                # Fallback suggestions
                return [
                    "Send personalized follow-up email",
                    "Schedule discovery call",
                    "Connect on LinkedIn",
                    "Add to email nurture sequence"
                ]
                
        except Exception as e:
            logger.error(f"Error generating follow-up suggestions: {str(e)}")
            return ["Send follow-up email", "Schedule phone call", "Add to nurture campaign"]

    def test_connection(self):
        """Test OpenAI API connection"""
        if not self.enabled:
            return False

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {str(e)}")
            return False

# Global instance
openai_service = OpenAIService()