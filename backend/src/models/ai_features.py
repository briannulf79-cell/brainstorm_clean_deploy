from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime
import json

db = SQLAlchemy()

class AILeadScore(db.Model):
    __tablename__ = 'ai_lead_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 0-100
    confidence = db.Column(db.Float, default=0.0)  # 0.0-1.0
    factors = db.Column(db.Text)  # JSON array of scoring factors
    model_version = db.Column(db.String(50), default='v1.0')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contact = db.relationship('Contact', backref='ai_scores')
    
    def __repr__(self):
        return f'<AILeadScore contact_id={self.contact_id} score={self.score}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'score': self.score,
            'confidence': self.confidence,
            'factors': json.loads(self.factors) if self.factors else [],
            'model_version': self.model_version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AIInsight(db.Model):
    __tablename__ = 'ai_insights'
    
    id = db.Column(db.Integer, primary_key=True)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # recommendation, prediction, alert, optimization
    category = db.Column(db.String(50))  # sales, marketing, customer_service, etc.
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    data = db.Column(db.Text)  # JSON data supporting the insight
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(20), default='active')  # active, dismissed, implemented
    confidence_score = db.Column(db.Float, default=0.0)
    potential_impact = db.Column(db.String(50))  # revenue, efficiency, conversion, etc.
    estimated_value = db.Column(Numeric(10, 2))  # estimated monetary impact
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<AIInsight {self.type}: {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'type': self.type,
            'category': self.category,
            'title': self.title,
            'description': self.description,
            'data': json.loads(self.data) if self.data else {},
            'priority': self.priority,
            'status': self.status,
            'confidence_score': self.confidence_score,
            'potential_impact': self.potential_impact,
            'estimated_value': float(self.estimated_value) if self.estimated_value else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

class AutomationWorkflow(db.Model):
    __tablename__ = 'automation_workflows'
    
    id = db.Column(db.Integer, primary_key=True)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    trigger_type = db.Column(db.String(50), nullable=False)  # form_submit, email_open, tag_added, etc.
    trigger_config = db.Column(db.Text)  # JSON configuration for trigger
    workflow_steps = db.Column(db.Text)  # JSON array of workflow steps
    status = db.Column(db.String(20), default='draft')  # draft, active, paused, archived
    is_ai_optimized = db.Column(db.Boolean, default=False)
    performance_metrics = db.Column(db.Text)  # JSON object with metrics
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    executions = db.relationship('WorkflowExecution', backref='workflow', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<AutomationWorkflow {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'name': self.name,
            'description': self.description,
            'trigger_type': self.trigger_type,
            'trigger_config': json.loads(self.trigger_config) if self.trigger_config else {},
            'workflow_steps': json.loads(self.workflow_steps) if self.workflow_steps else [],
            'status': self.status,
            'is_ai_optimized': self.is_ai_optimized,
            'performance_metrics': json.loads(self.performance_metrics) if self.performance_metrics else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'executions_count': len(self.executions)
        }

class WorkflowExecution(db.Model):
    __tablename__ = 'workflow_executions'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('automation_workflows.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    trigger_data = db.Column(db.Text)  # JSON data that triggered the workflow
    status = db.Column(db.String(20), default='running')  # running, completed, failed, cancelled
    current_step = db.Column(db.Integer, default=0)
    execution_log = db.Column(db.Text)  # JSON array of execution steps
    error_message = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<WorkflowExecution workflow_id={self.workflow_id} status={self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'contact_id': self.contact_id,
            'trigger_data': json.loads(self.trigger_data) if self.trigger_data else {},
            'status': self.status,
            'current_step': self.current_step,
            'execution_log': json.loads(self.execution_log) if self.execution_log else [],
            'error_message': self.error_message,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class AIConversation(db.Model):
    __tablename__ = 'ai_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
    ai_agent_type = db.Column(db.String(50), default='chatbot')  # chatbot, voice_assistant, email_assistant
    context = db.Column(db.Text)  # JSON context for AI conversation
    sentiment_score = db.Column(db.Float)  # -1.0 to 1.0
    intent_classification = db.Column(db.String(100))
    confidence_score = db.Column(db.Float)
    requires_human_handoff = db.Column(db.Boolean, default=False)
    handoff_reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AIConversation contact_id={self.contact_id} type={self.ai_agent_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'conversation_id': self.conversation_id,
            'ai_agent_type': self.ai_agent_type,
            'context': json.loads(self.context) if self.context else {},
            'sentiment_score': self.sentiment_score,
            'intent_classification': self.intent_classification,
            'confidence_score': self.confidence_score,
            'requires_human_handoff': self.requires_human_handoff,
            'handoff_reason': self.handoff_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PredictiveAnalytics(db.Model):
    __tablename__ = 'predictive_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    sub_account_id = db.Column(db.Integer, db.ForeignKey('sub_accounts.id'), nullable=False)
    model_type = db.Column(db.String(50), nullable=False)  # churn_prediction, revenue_forecast, lead_conversion
    prediction_data = db.Column(db.Text)  # JSON prediction results
    confidence_interval = db.Column(db.Text)  # JSON confidence intervals
    model_accuracy = db.Column(db.Float)
    prediction_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PredictiveAnalytics {self.model_type} for {self.prediction_date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sub_account_id': self.sub_account_id,
            'model_type': self.model_type,
            'prediction_data': json.loads(self.prediction_data) if self.prediction_data else {},
            'confidence_interval': json.loads(self.confidence_interval) if self.confidence_interval else {},
            'model_accuracy': self.model_accuracy,
            'prediction_date': self.prediction_date.isoformat() if self.prediction_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

