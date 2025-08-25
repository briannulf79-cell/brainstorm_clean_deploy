import json
from datetime import datetime, timedelta
from models import db, User, Contact
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemoService:
    """Service to manage demo data isolation"""
    
    def seed_demo_data(self):
        """Seed demo data ONLY for demo user"""
        try:
            demo_user = User.query.filter_by(email='demo@brainstormaikit.com').first()
            if not demo_user:
                logger.warning("Demo user not found")
                return False
            
            # Check if demo data already exists
            existing_contacts = Contact.query.filter_by(sub_account_id=demo_user.id).count()
            if existing_contacts > 0:
                logger.info("Demo data already exists")
                return True
            
            # Create demo contacts
            demo_contacts = [
                {
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'email': 'john.smith@techcorp.com',
                    'phone': '+1-555-0101',
                    'company': 'TechCorp Solutions',
                    'source': 'website',
                    'status': 'active',
                    'lead_score': 85.0,
                    'tags': json.dumps(['hot-lead', 'enterprise']),
                    'notes': 'Interested in enterprise package. Decision maker for IT infrastructure.',
                    'activities_count': 8
                },
                {
                    'first_name': 'Sarah',
                    'last_name': 'Johnson',
                    'email': 'sarah@marketingpro.co',
                    'phone': '+1-555-0102',
                    'company': 'Marketing Pro Agency',
                    'source': 'referral',
                    'status': 'active',
                    'lead_score': 92.0,
                    'tags': json.dumps(['qualified', 'agency']),
                    'notes': 'Agency owner looking for white-label solution. Very engaged.',
                    'activities_count': 12
                },
                {
                    'first_name': 'Mike',
                    'last_name': 'Chen',
                    'email': 'mike.chen@startup.io',
                    'phone': '+1-555-0103',
                    'company': 'StartupXYZ',
                    'source': 'social_media',
                    'status': 'active',
                    'lead_score': 70.0,
                    'tags': json.dumps(['startup', 'warm-lead']),
                    'notes': 'Startup founder. Budget conscious but high growth potential.',
                    'activities_count': 5
                },
                {
                    'first_name': 'Lisa',
                    'last_name': 'Williams',
                    'email': 'lisa@consulting.biz',
                    'phone': '+1-555-0104',
                    'company': 'Williams Consulting',
                    'source': 'google_ads',
                    'status': 'active',
                    'lead_score': 78.0,
                    'tags': json.dumps(['consultant', 'interested']),
                    'notes': 'Business consultant. Needs CRM for client management.',
                    'activities_count': 6
                },
                {
                    'first_name': 'David',
                    'last_name': 'Brown',
                    'email': 'david@realestate.com',
                    'phone': '+1-555-0105',
                    'company': 'Brown Real Estate',
                    'source': 'trade_show',
                    'status': 'active',
                    'lead_score': 65.0,
                    'tags': json.dumps(['real-estate', 'cold-lead']),
                    'notes': 'Real estate agent. Met at trade show. Needs follow-up.',
                    'activities_count': 3
                }
            ]
            
            for contact_data in demo_contacts:
                contact = Contact(
                    sub_account_id=demo_user.id,  # Link to demo user's account
                    **contact_data
                )
                db.session.add(contact)
            
            db.session.commit()
            logger.info(f"Successfully seeded {len(demo_contacts)} demo contacts")
            return True
            
        except Exception as e:
            logger.error(f"Error seeding demo data: {str(e)}")
            db.session.rollback()
            return False
    
    def is_demo_user(self, user):
        """Check if user is the demo user"""
        return user.email == 'demo@brainstormaikit.com'
    
    def get_user_contacts(self, user):
        """Get contacts for user - demo data only for demo user"""
        if self.is_demo_user(user):
            # Ensure demo data exists
            if Contact.query.filter_by(sub_account_id=user.id).count() == 0:
                self.seed_demo_data()
            
            return Contact.query.filter_by(sub_account_id=user.id).all()
        else:
            # For all other users, return their own contacts
            return Contact.query.filter_by(sub_account_id=user.id).all()
    
    def clean_user_account(self, user):
        """Ensure user account starts clean (non-demo users only)"""
        if self.is_demo_user(user):
            return  # Don't clean demo user
            
        try:
            # Remove any existing contacts for this user
            Contact.query.filter_by(sub_account_id=user.id).delete()
            db.session.commit()
            logger.info(f"Cleaned account for user {user.email}")
        except Exception as e:
            logger.error(f"Error cleaning user account {user.email}: {str(e)}")
            db.session.rollback()

# Global instance
demo_service = DemoService()