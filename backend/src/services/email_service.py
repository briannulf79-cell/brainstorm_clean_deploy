import os
import requests
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.api_key = os.environ.get('MAILGUN_API_KEY')
        self.domain = os.environ.get('MAILGUN_DOMAIN')
        self.from_email = os.environ.get('FROM_EMAIL', 'noreply@brainstormaikit.com')
        
        if not self.api_key or not self.domain:
            logger.warning("Mailgun API key or domain not configured. Email functionality will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
            self.base_url = f"https://api.mailgun.net/v3/{self.domain}"

    def send_email(self, to_email, subject, html_content, text_content=None):
        """Send an email using Mailgun API"""
        if not self.enabled:
            logger.warning(f"Email service disabled. Would have sent: {subject} to {to_email}")
            return False

        try:
            data = {
                'from': self.from_email,
                'to': to_email,
                'subject': subject,
                'html': html_content
            }
            
            if text_content:
                data['text'] = text_content

            response = requests.post(
                f"{self.base_url}/messages",
                auth=("api", self.api_key),
                data=data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email to {to_email}: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Exception sending email to {to_email}: {str(e)}")
            return False

    def send_welcome_email(self, user_email, user_name):
        """Send welcome email to new users"""
        subject = "Welcome to Brainstorm AI Kit - Your 30-Day Trial Starts Now!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ margin-top: 30px; text-align: center; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧠 Welcome to Brainstorm AI Kit!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name}!</h2>
                    <p>Welcome to your AI-powered CRM and marketing automation platform. Your <strong>30-day free trial</strong> has officially started!</p>
                    
                    <h3>🚀 What you can do right now:</h3>
                    <ul>
                        <li>📊 Create unlimited contacts and manage your CRM</li>
                        <li>🤖 Use AI-powered lead scoring and insights</li>
                        <li>📧 Build automated email campaigns</li>
                        <li>📱 Send SMS campaigns via Twilio integration</li>
                        <li>🌐 Create unlimited websites with our builder</li>
                        <li>📈 Track performance with advanced analytics</li>
                    </ul>
                    
                    <div style="text-align: center;">
                        <a href="https://app.brainstormaikit.com/dashboard" class="button">Get Started Now</a>
                    </div>
                    
                    <p><strong>Need help?</strong> Our support team is here to help you succeed. Simply reply to this email with any questions.</p>
                    
                    <p>Best regards,<br>The Brainstorm AI Kit Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent to {user_email}</p>
                    <p>Brainstorm AI Kit - AI-Powered Business Growth</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to Brainstorm AI Kit!
        
        Hi {user_name}!
        
        Welcome to your AI-powered CRM and marketing automation platform. Your 30-day free trial has officially started!
        
        What you can do right now:
        - Create unlimited contacts and manage your CRM
        - Use AI-powered lead scoring and insights  
        - Build automated email campaigns
        - Send SMS campaigns via Twilio integration
        - Create unlimited websites with our builder
        - Track performance with advanced analytics
        
        Get started: https://app.brainstormaikit.com/dashboard
        
        Need help? Our support team is here to help you succeed. Simply reply to this email with any questions.
        
        Best regards,
        The Brainstorm AI Kit Team
        """
        
        return self.send_email(user_email, subject, html_content, text_content)

    def send_trial_warning_email(self, user_email, user_name, days_remaining):
        """Send trial expiration warning email"""
        if days_remaining == 7:
            subject = "⏰ Your Brainstorm AI Kit trial expires in 7 days"
            urgency = "You have one week left"
        elif days_remaining == 1:
            subject = "🚨 Last chance! Your trial expires tomorrow"
            urgency = "Your trial expires in just 24 hours"
        else:
            subject = f"⏰ Your Brainstorm AI Kit trial expires in {days_remaining} days"
            urgency = f"You have {days_remaining} days left"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #ff9a56 0%, #ff6b6b 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ margin-top: 30px; text-align: center; color: #666; font-size: 14px; }}
                .urgent {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ Trial Ending Soon</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name}!</h2>
                    
                    <div class="urgent">
                        <strong>{urgency}</strong> to continue using all the powerful features of Brainstorm AI Kit.
                    </div>
                    
                    <p>We hope you've been loving your experience with our AI-powered CRM and marketing automation platform!</p>
                    
                    <h3>🎯 Don't lose access to:</h3>
                    <ul>
                        <li>📊 Your CRM data and contacts</li>
                        <li>🤖 AI-powered insights and automation</li>
                        <li>📧 Email marketing campaigns</li>
                        <li>📱 SMS marketing via Twilio</li>
                        <li>🌐 Your websites and funnels</li>
                        <li>📈 Analytics and reporting</li>
                    </ul>
                    
                    <div style="text-align: center;">
                        <a href="https://app.brainstormaikit.com/upgrade" class="button">Upgrade Now - From $97/month</a>
                    </div>
                    
                    <p><strong>Questions?</strong> Reply to this email or contact our support team. We're here to help!</p>
                    
                    <p>Best regards,<br>The Brainstorm AI Kit Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent to {user_email}</p>
                    <p>Don't want these reminders? <a href="#">Update your preferences</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)

    def send_trial_expired_email(self, user_email, user_name):
        """Send trial expired notification"""
        subject = "Your Brainstorm AI Kit trial has expired"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #6c757d; color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Trial Expired</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name}!</h2>
                    <p>Your 30-day free trial of Brainstorm AI Kit has ended. We hope you enjoyed exploring all the powerful features!</p>
                    
                    <p><strong>Your data is safe</strong> - we've preserved all your contacts, campaigns, and settings. Simply upgrade to continue where you left off.</p>
                    
                    <div style="text-align: center;">
                        <a href="https://app.brainstormaikit.com/upgrade" class="button">Upgrade to Continue</a>
                    </div>
                    
                    <p>Questions about upgrading? Reply to this email and we'll help you choose the perfect plan.</p>
                    
                    <p>Thank you for trying Brainstorm AI Kit!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)

    def send_password_reset_email(self, user_email, reset_token):
        """Send password reset email"""
        subject = "Reset your Brainstorm AI Kit password"
        reset_url = f"https://app.brainstormaikit.com/reset-password?token={reset_token}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #667eea; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Reset Request</h1>
                </div>
                <div class="content">
                    <p>You requested a password reset for your Brainstorm AI Kit account.</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_url}" class="button">Reset Password</a>
                    </div>
                    
                    <p>This link will expire in 1 hour for security reasons.</p>
                    
                    <p>If you didn't request this reset, please ignore this email. Your password will remain unchanged.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)

# Global instance
email_service = EmailService()