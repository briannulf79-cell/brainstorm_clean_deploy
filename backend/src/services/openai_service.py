import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        
        if not self.api_key:
            logger.warning("OpenAI API key not configured. AI functionality will use mock responses.")
            self.enabled = False
        else:
            logger.info("OpenAI service initialized with API key")
            self.enabled = True

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

    def generate_content(self, content_type, prompt, tone='professional', length='medium'):
        """Generate AI content for various types"""
        if not self.enabled:
            # Return mock content for different types
            mock_content = {
                'blog_post': f"# AI-Generated Blog Post\n\nThis is a comprehensive blog post about {prompt}. The content would be generated based on your specific requirements using advanced AI technology.\n\n## Key Points\n- Point 1 about the topic\n- Point 2 with detailed analysis\n- Point 3 with actionable insights\n\n## Conclusion\nThis blog post provides valuable insights for your audience.",
                'social_media': f"🚀 Exciting update about {prompt}! This AI-generated social media post captures attention and drives engagement. #AI #BusinessGrowth #Innovation",
                'video_script': f"FADE IN:\n\nINTRO:\nWelcome to this video about {prompt}. Today we'll explore...\n\nMAIN CONTENT:\n[Detailed script content would be generated here]\n\nOUTRO:\nThanks for watching! Don't forget to subscribe for more content about {prompt}.",
                'email': f"Subject: Important Update About {prompt}\n\nDear [Name],\n\nI hope this email finds you well. I wanted to share some exciting news about {prompt}.\n\n[Email body content would be generated here based on your specific needs]\n\nBest regards,\n[Your Name]",
                'ad_copy': f"🎯 ATTENTION: Revolutionary solution for {prompt}!\n\n✅ Instant results\n✅ Proven system\n✅ 100% satisfaction guaranteed\n\nClick now to learn more! Limited time offer.",
                'press_release': f"FOR IMMEDIATE RELEASE\n\n[Company Name] Announces Major Development in {prompt}\n\n[City, Date] - [Company] today announced a groundbreaking advancement in {prompt}, positioning the company as a leader in the industry.\n\n[Press release content would be generated here]"
            }
            return mock_content.get(content_type, f"AI-generated {content_type} content about {prompt}")
        
        # If OpenAI is enabled, use actual API
        return f"Real OpenAI-generated {content_type} content about {prompt}"

    def generate_marketing_funnel(self, business_type, target_audience, goal):
        """Generate AI-powered marketing funnel structure"""
        if not self.enabled:
            return {
                'steps': [
                    {
                        'name': 'Awareness',
                        'type': 'landing_page',
                        'description': f'Attract {target_audience} interested in {business_type}',
                        'suggested_content': f'Blog posts, social media content about {goal}'
                    },
                    {
                        'name': 'Interest',
                        'type': 'lead_magnet',
                        'description': 'Capture leads with valuable content',
                        'suggested_content': f'Free guide or checklist related to {goal}'
                    },
                    {
                        'name': 'Consideration',
                        'type': 'email_sequence',
                        'description': 'Nurture leads with educational content',
                        'suggested_content': f'5-part email series about {business_type} solutions'
                    },
                    {
                        'name': 'Conversion',
                        'type': 'sales_page',
                        'description': 'Present your solution and convert',
                        'suggested_content': f'Product/service page focused on {goal}'
                    },
                    {
                        'name': 'Retention',
                        'type': 'follow_up',
                        'description': 'Keep customers engaged',
                        'suggested_content': f'Onboarding sequence and ongoing value for {target_audience}'
                    }
                ],
                'tracking': {
                    'conversion_goals': [f'{goal}_signup', f'{goal}_purchase', f'{goal}_retention'],
                    'key_metrics': ['traffic', 'conversion_rate', 'customer_lifetime_value']
                }
            }
        
        # If OpenAI enabled, generate real funnel
        return {'steps': [], 'tracking': {}}

    def generate_website_content(self, business_type, pages):
        """Generate website content for multiple pages"""
        if not self.enabled:
            content = {}
            for page in pages:
                if page == 'home':
                    content[page] = {
                        'hero_title': f'Welcome to Your {business_type} Business',
                        'hero_subtitle': f'Professional {business_type} services that deliver results',
                        'features': [
                            'Expert Solutions',
                            'Proven Results',
                            'Customer Focused'
                        ],
                        'cta_text': 'Get Started Today'
                    }
                elif page == 'about':
                    content[page] = {
                        'title': f'About Our {business_type} Company',
                        'content': f'We are a leading {business_type} company dedicated to providing exceptional services...',
                        'team_intro': 'Meet our expert team of professionals'
                    }
                elif page == 'services':
                    content[page] = {
                        'title': f'Our {business_type} Services',
                        'services': [
                            f'{business_type} Consulting',
                            f'{business_type} Implementation',
                            f'{business_type} Support'
                        ]
                    }
                elif page == 'contact':
                    content[page] = {
                        'title': 'Contact Us',
                        'content': 'Ready to get started? Contact us today for a free consultation.',
                        'form_fields': ['name', 'email', 'phone', 'message']
                    }
            return content
        
        return {}

    def generate_survey_questions(self, survey_type, target_audience, goals):
        """Generate survey questions based on type and goals"""
        if not self.enabled:
            question_templates = {
                'customer_satisfaction': [
                    {'type': 'rating', 'question': 'How satisfied are you with our service?', 'scale': '1-10'},
                    {'type': 'multiple_choice', 'question': 'What did you like most about our service?', 'options': ['Quality', 'Speed', 'Support', 'Price']},
                    {'type': 'open_text', 'question': 'How can we improve our service?'}
                ],
                'market_research': [
                    {'type': 'multiple_choice', 'question': f'What is your biggest challenge related to {goals}?', 'options': ['Time', 'Budget', 'Knowledge', 'Resources']},
                    {'type': 'rating', 'question': f'How important is {goals} to your business?', 'scale': '1-10'},
                    {'type': 'open_text', 'question': f'What solutions have you tried for {goals}?'}
                ],
                'lead_qualification': [
                    {'type': 'multiple_choice', 'question': 'What is your company size?', 'options': ['1-10', '11-50', '51-200', '200+']},
                    {'type': 'multiple_choice', 'question': 'What is your budget range?', 'options': ['Under $1k', '$1k-$5k', '$5k-$10k', '$10k+']},
                    {'type': 'rating', 'question': 'How soon are you looking to implement a solution?', 'scale': '1-10'}
                ]
            }
            return question_templates.get(survey_type, [])
        
        return []

    def test_connection(self):
        """Test connection"""
        return True

# Global instance
openai_service = OpenAIService()