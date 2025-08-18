import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from src.models.user import db

# Import models in correct order to resolve foreign key dependencies
from src.models.agency import Agency, SubAccount, UserPermission
from src.models.user import User
from src.models.contact import Contact, ContactActivity, ContactNote, ContactTask
from src.models.pipeline import Pipeline, Opportunity, OpportunityActivity
from src.models.campaign import Campaign, Conversation, Message
from src.models.ai_features import AILeadScore, AIInsight, AutomationWorkflow, WorkflowExecution, AIConversation, PredictiveAnalytics
from src.models.integrations import Integration, WebsiteBuilder, WebsiteForm, FormSubmission, OnlineCourse, CourseLesson, CourseEnrollment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully!")
    
    # Create default data
    from src.utils.seed_data import create_default_data
    create_default_data()
    print("Default data created successfully!")

