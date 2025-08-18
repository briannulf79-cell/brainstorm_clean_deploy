from src.models.user import db, User
from src.models.agency import Agency, SubAccount
from src.models.contact import Contact, ContactActivity
from src.models.pipeline import Pipeline, Opportunity
from src.models.campaign import Campaign
from datetime import datetime, timedelta
import json

def create_default_data():
    """Create default data for demo purposes"""
    
    # Check if data already exists
    if User.query.first():
        return
    
    try:
        # Create demo agency
        agency = Agency(
            name="Brainstorm AI Kit Demo",
            domain="demo.brainstormaikit.com",
            plan_type="unlimited",
            branding_config=json.dumps({
                "primary_color": "#3b82f6",
                "secondary_color": "#1e293b",
                "logo_url": "/assets/logo.png",
                "company_name": "Brainstorm AI Kit"
            })
        )
        db.session.add(agency)
        db.session.flush()
        
        # Create demo user
        user = User(
            email="demo@brainstormaikit.com",
            first_name="Demo",
            last_name="User",
            role="admin",
            agency_id=agency.id,
            phone="+1-555-0123"
        )
        user.set_password("demo123")
        db.session.add(user)
        db.session.flush()
        
        # Create demo sub-account
        sub_account = SubAccount(
            agency_id=agency.id,
            name="Demo Business",
            industry="technology",
            settings=json.dumps({
                "timezone": "America/New_York",
                "currency": "USD",
                "ai_features_enabled": True
            })
        )
        db.session.add(sub_account)
        db.session.flush()
        
        # Create demo pipeline
        pipeline = Pipeline(
            sub_account_id=sub_account.id,
            name="Sales Pipeline",
            stages=json.dumps([
                {"name": "Lead", "order": 0, "color": "#3b82f6", "probability": 10},
                {"name": "Qualified", "order": 1, "color": "#10b981", "probability": 25},
                {"name": "Proposal", "order": 2, "color": "#f59e0b", "probability": 50},
                {"name": "Negotiation", "order": 3, "color": "#ef4444", "probability": 75},
                {"name": "Closed Won", "order": 4, "color": "#22c55e", "probability": 100}
            ]),
            is_default=True
        )
        db.session.add(pipeline)
        db.session.flush()
        
        # Create demo contacts
        demo_contacts = [
            {
                "first_name": "John", "last_name": "Smith", "email": "john.smith@example.com",
                "phone": "+1-555-0101", "company": "Tech Innovations Inc", 
                "tags": ["hot_lead", "enterprise"], "source": "website"
            },
            {
                "first_name": "Sarah", "last_name": "Johnson", "email": "sarah.j@example.com",
                "phone": "+1-555-0102", "company": "Digital Marketing Pro", 
                "tags": ["qualified", "smb"], "source": "referral"
            },
            {
                "first_name": "Michael", "last_name": "Brown", "email": "m.brown@example.com",
                "phone": "+1-555-0103", "company": "Growth Solutions LLC", 
                "tags": ["customer", "recurring"], "source": "social_media"
            },
            {
                "first_name": "Emily", "last_name": "Davis", "email": "emily.davis@example.com",
                "phone": "+1-555-0104", "company": "Startup Accelerator", 
                "tags": ["prospect", "startup"], "source": "cold_outreach"
            },
            {
                "first_name": "David", "last_name": "Wilson", "email": "d.wilson@example.com",
                "phone": "+1-555-0105", "company": "Enterprise Corp", 
                "tags": ["enterprise", "decision_maker"], "source": "trade_show"
            }
        ]
        
        contacts = []
        for contact_data in demo_contacts:
            contact = Contact(
                sub_account_id=sub_account.id,
                first_name=contact_data["first_name"],
                last_name=contact_data["last_name"],
                email=contact_data["email"],
                phone=contact_data["phone"],
                company=contact_data["company"],
                tags=json.dumps(contact_data["tags"]),
                source=contact_data["source"],
                status="active",
                created_at=datetime.utcnow() - timedelta(days=30)
            )
            db.session.add(contact)
            contacts.append(contact)
        
        db.session.flush()
        
        # Create demo opportunities
        stages = ["Lead", "Qualified", "Proposal", "Negotiation", "Closed Won"]
        values = [25000, 45000, 15000, 75000, 35000]
        
        for i, contact in enumerate(contacts):
            opportunity = Opportunity(
                pipeline_id=pipeline.id,
                contact_id=contact.id,
                user_id=user.id,
                title=f"Deal with {contact.company}",
                description=f"Potential AI automation project for {contact.company}",
                stage=stages[i],
                value=values[i],
                probability=[10, 25, 50, 75, 100][i],
                status="won" if stages[i] == "Closed Won" else "open",
                source=contact.source,
                created_at=datetime.utcnow() - timedelta(days=20)
            )
            db.session.add(opportunity)
        
        # Create demo campaigns
        campaigns = [
            {
                "name": "AI Solutions Newsletter",
                "type": "email",
                "status": "active",
                "subject": "Transform Your Business with AI Automation"
            },
            {
                "name": "Lead Nurture Sequence",
                "type": "mixed",
                "status": "active",
                "subject": "Your AI Journey Starts Here"
            },
            {
                "name": "Product Demo Follow-up",
                "type": "sms",
                "status": "completed",
                "subject": "Thanks for your interest in Brainstorm AI Kit"
            }
        ]
        
        for campaign_data in campaigns:
            campaign = Campaign(
                sub_account_id=sub_account.id,
                name=campaign_data["name"],
                type=campaign_data["type"],
                status=campaign_data["status"],
                subject=campaign_data["subject"],
                content="Demo campaign content",
                created_at=datetime.utcnow() - timedelta(days=15)
            )
            db.session.add(campaign)
        
        db.session.commit()
        print("Demo data created successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating demo data: {e}")

