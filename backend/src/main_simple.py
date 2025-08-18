import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'agile_ai_solutions_secret_key_2024'

# Enable CORS for all routes
CORS(app, origins="*")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Simple User model for demo
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Simple Contact model for demo
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()
    
    # Create demo user if not exists
    if not User.query.filter_by(email='demo@brainstormaikit.com').first():
        demo_user = User(
            email='demo@brainstormaikit.com',
            password='demo123',
            first_name='Demo',
            last_name='User'
        )
        db.session.add(demo_user)
        db.session.commit()

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'service': 'Brainstorm AI Kit API', 'version': '1.0.0'}

@app.route('/api/auth/login', methods=['POST'])
def login():
    return {
        'success': True,
        'user': {
            'id': 1,
            'email': 'demo@brainstormaikit.com',
            'first_name': 'Demo',
            'last_name': 'User'
        },
        'token': 'demo_token_123'
    }

@app.route('/api/dashboard/overview', methods=['GET'])
def dashboard_overview():
    return {
        'total_contacts': 2847,
        'new_contacts_this_month': 156,
        'total_revenue': 125000,
        'revenue_growth': 12.5,
        'active_campaigns': 8,
        'conversion_rate': 3.2
    }

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return {
        'contacts': [
            {
                'id': c.id,
                'first_name': c.first_name,
                'last_name': c.last_name,
                'email': c.email,
                'phone': c.phone,
                'company': c.company,
                'created_at': c.created_at.isoformat() if c.created_at else None
            } for c in contacts
        ],
        'total': len(contacts)
    }

@app.route('/api/analytics/overview', methods=['GET'])
def analytics_overview():
    return {
        'total_contacts': 2847,
        'new_contacts': 156,
        'total_revenue': 125000,
        'revenue_growth': 12.5,
        'conversion_rate': 3.2,
        'conversion_change': 0.8,
        'avg_deal_size': 4500,
        'deal_size_change': -2.1
    }

@app.route('/api/ai/insights', methods=['GET'])
def ai_insights():
    return {
        'insights': [
            {
                'type': 'performance',
                'title': 'Strong Performance Detected',
                'description': 'Your conversion rate is 23% above industry average.',
                'confidence': 87,
                'impact': 'positive'
            },
            {
                'type': 'opportunity',
                'title': 'Social Media Optimization',
                'description': 'Consider A/B testing different messaging approaches.',
                'confidence': 73,
                'impact': 'neutral'
            }
        ]
    }

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

