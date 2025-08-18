from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.ai_features import AILeadScore, AIInsight, AutomationWorkflow, WorkflowExecution, AIConversation, PredictiveAnalytics
from src.models.contact import Contact
from datetime import datetime, timedelta
import json
import random

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/lead-scoring', methods=['POST'])
def calculate_lead_score():
    """Calculate AI-powered lead score for a contact"""
    try:
        data = request.get_json()
        contact_id = data.get('contact_id')
        
        if not contact_id:
            return jsonify({'error': 'contact_id is required'}), 400
        
        contact = Contact.query.get_or_404(contact_id)
        
        # Mock AI scoring algorithm - in production, this would use ML models
        score_factors = []
        base_score = 50
        
        # Email domain scoring
        if contact.email:
            domain = contact.email.split('@')[1] if '@' in contact.email else ''
            if domain in ['gmail.com', 'yahoo.com', 'hotmail.com']:
                base_score -= 10
                score_factors.append({'factor': 'Personal email domain', 'impact': -10})
            else:
                base_score += 15
                score_factors.append({'factor': 'Business email domain', 'impact': 15})
        
        # Company presence
        if contact.company:
            base_score += 20
            score_factors.append({'factor': 'Company information provided', 'impact': 20})
        
        # Phone number
        if contact.phone:
            base_score += 10
            score_factors.append({'factor': 'Phone number provided', 'impact': 10})
        
        # Tags analysis
        if contact.tags:
            tags = json.loads(contact.tags)
            if 'enterprise' in tags:
                base_score += 25
                score_factors.append({'factor': 'Enterprise tag', 'impact': 25})
            if 'hot_lead' in tags:
                base_score += 30
                score_factors.append({'factor': 'Hot lead tag', 'impact': 30})
            if 'customer' in tags:
                base_score += 40
                score_factors.append({'factor': 'Existing customer', 'impact': 40})
        
        # Source scoring
        source_scores = {
            'referral': 25,
            'website': 15,
            'social_media': 10,
            'cold_outreach': -5,
            'trade_show': 20
        }
        if contact.source and contact.source in source_scores:
            impact = source_scores[contact.source]
            base_score += impact
            score_factors.append({'factor': f'Lead source: {contact.source}', 'impact': impact})
        
        # Ensure score is within bounds
        final_score = max(0, min(100, base_score))
        confidence = 0.85  # Mock confidence score
        
        # Save or update lead score
        existing_score = AILeadScore.query.filter_by(contact_id=contact_id).first()
        if existing_score:
            existing_score.score = final_score
            existing_score.confidence = confidence
            existing_score.factors = json.dumps(score_factors)
            existing_score.updated_at = datetime.utcnow()
        else:
            lead_score = AILeadScore(
                contact_id=contact_id,
                score=final_score,
                confidence=confidence,
                factors=json.dumps(score_factors)
            )
            db.session.add(lead_score)
        
        db.session.commit()
        
        return jsonify({
            'contact_id': contact_id,
            'score': final_score,
            'confidence': confidence,
            'factors': score_factors,
            'recommendation': 'High priority' if final_score >= 80 else 'Medium priority' if final_score >= 60 else 'Low priority'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/insights', methods=['GET'])
def get_ai_insights():
    """Get AI-generated insights for a sub-account"""
    try:
        sub_account_id = request.args.get('sub_account_id', type=int)
        category = request.args.get('category')
        priority = request.args.get('priority')
        
        query = AIInsight.query
        if sub_account_id:
            query = query.filter_by(sub_account_id=sub_account_id)
        if category:
            query = query.filter_by(category=category)
        if priority:
            query = query.filter_by(priority=priority)
        
        insights = query.filter_by(status='active').order_by(
            AIInsight.priority.desc(), AIInsight.created_at.desc()
        ).limit(20).all()
        
        return jsonify({
            'insights': [insight.to_dict() for insight in insights]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/insights/generate', methods=['POST'])
def generate_insights():
    """Generate new AI insights for a sub-account"""
    try:
        data = request.get_json()
        sub_account_id = data.get('sub_account_id')
        
        if not sub_account_id:
            return jsonify({'error': 'sub_account_id is required'}), 400
        
        # Mock insight generation - in production, this would analyze real data
        sample_insights = [
            {
                'type': 'recommendation',
                'category': 'sales',
                'title': 'Optimize Follow-up Timing',
                'description': 'Contacts respond 40% better to follow-ups sent on Tuesday mornings between 9-11 AM.',
                'priority': 'high',
                'potential_impact': 'conversion',
                'estimated_value': 2500.00,
                'confidence_score': 0.87
            },
            {
                'type': 'prediction',
                'category': 'marketing',
                'title': 'Campaign Performance Forecast',
                'description': 'Your email campaign is predicted to achieve 18% open rate and 3.2% click-through rate.',
                'priority': 'medium',
                'potential_impact': 'efficiency',
                'estimated_value': 1200.00,
                'confidence_score': 0.73
            },
            {
                'type': 'alert',
                'category': 'customer_service',
                'title': 'Potential Churn Risk',
                'description': '3 high-value customers show decreased engagement patterns similar to churned customers.',
                'priority': 'critical',
                'potential_impact': 'revenue',
                'estimated_value': 15000.00,
                'confidence_score': 0.91
            }
        ]
        
        created_insights = []
        for insight_data in sample_insights:
            insight = AIInsight(
                sub_account_id=sub_account_id,
                type=insight_data['type'],
                category=insight_data['category'],
                title=insight_data['title'],
                description=insight_data['description'],
                priority=insight_data['priority'],
                potential_impact=insight_data['potential_impact'],
                estimated_value=insight_data['estimated_value'],
                confidence_score=insight_data['confidence_score'],
                expires_at=datetime.utcnow() + timedelta(days=7)
            )
            db.session.add(insight)
            created_insights.append(insight)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Generated {len(created_insights)} new insights',
            'insights': [insight.to_dict() for insight in created_insights]
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/workflows', methods=['GET'])
def get_automation_workflows():
    """Get automation workflows"""
    try:
        sub_account_id = request.args.get('sub_account_id', type=int)
        
        query = AutomationWorkflow.query
        if sub_account_id:
            query = query.filter_by(sub_account_id=sub_account_id)
        
        workflows = query.order_by(AutomationWorkflow.created_at.desc()).all()
        
        return jsonify({
            'workflows': [workflow.to_dict() for workflow in workflows]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/workflows', methods=['POST'])
def create_automation_workflow():
    """Create a new automation workflow"""
    try:
        data = request.get_json()
        
        required_fields = ['sub_account_id', 'name', 'trigger_type', 'workflow_steps']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        workflow = AutomationWorkflow(
            sub_account_id=data['sub_account_id'],
            name=data['name'],
            description=data.get('description'),
            trigger_type=data['trigger_type'],
            trigger_config=json.dumps(data.get('trigger_config', {})),
            workflow_steps=json.dumps(data['workflow_steps']),
            status=data.get('status', 'draft'),
            is_ai_optimized=data.get('is_ai_optimized', False)
        )
        
        db.session.add(workflow)
        db.session.commit()
        
        return jsonify({
            'message': 'Workflow created successfully',
            'workflow': workflow.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/workflows/<int:workflow_id>/optimize', methods=['POST'])
def optimize_workflow():
    """AI-optimize an existing workflow"""
    try:
        workflow = AutomationWorkflow.query.get_or_404(workflow_id)
        
        # Mock AI optimization - in production, this would analyze performance data
        current_steps = json.loads(workflow.workflow_steps) if workflow.workflow_steps else []
        
        # Add AI-suggested optimizations
        optimizations = [
            {
                'type': 'timing_optimization',
                'description': 'Adjusted email send times based on recipient behavior patterns',
                'impact': 'Estimated 15% improvement in open rates'
            },
            {
                'type': 'content_personalization',
                'description': 'Added dynamic content blocks based on contact attributes',
                'impact': 'Estimated 25% improvement in click-through rates'
            },
            {
                'type': 'path_optimization',
                'description': 'Added conditional logic to skip steps for engaged contacts',
                'impact': 'Estimated 20% reduction in workflow completion time'
            }
        ]
        
        # Update workflow
        workflow.is_ai_optimized = True
        workflow.performance_metrics = json.dumps({
            'optimizations_applied': optimizations,
            'optimization_date': datetime.utcnow().isoformat(),
            'expected_improvements': {
                'open_rate': 15,
                'click_rate': 25,
                'completion_time': -20
            }
        })
        workflow.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Workflow optimized successfully',
            'optimizations': optimizations,
            'workflow': workflow.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/conversation-analysis', methods=['POST'])
def analyze_conversation():
    """Analyze conversation with AI for sentiment and intent"""
    try:
        data = request.get_json()
        contact_id = data.get('contact_id')
        conversation_id = data.get('conversation_id')
        message_content = data.get('message_content')
        
        if not all([contact_id, message_content]):
            return jsonify({'error': 'contact_id and message_content are required'}), 400
        
        # Mock AI analysis - in production, this would use NLP models
        sentiment_keywords = {
            'positive': ['great', 'excellent', 'love', 'amazing', 'perfect', 'thank you'],
            'negative': ['terrible', 'awful', 'hate', 'worst', 'disappointed', 'frustrated'],
            'neutral': ['okay', 'fine', 'maybe', 'perhaps', 'consider']
        }
        
        content_lower = message_content.lower()
        sentiment_score = 0.0
        
        for sentiment, keywords in sentiment_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    if sentiment == 'positive':
                        sentiment_score += 0.3
                    elif sentiment == 'negative':
                        sentiment_score -= 0.3
        
        # Normalize sentiment score
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        # Intent classification
        intent_keywords = {
            'purchase_intent': ['buy', 'purchase', 'price', 'cost', 'order'],
            'support_request': ['help', 'problem', 'issue', 'support', 'broken'],
            'information_request': ['how', 'what', 'when', 'where', 'why', 'tell me'],
            'complaint': ['complain', 'unhappy', 'dissatisfied', 'refund']
        }
        
        intent_classification = 'general'
        confidence_score = 0.5
        
        for intent, keywords in intent_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in content_lower)
            if matches > 0:
                intent_classification = intent
                confidence_score = min(0.95, 0.5 + (matches * 0.15))
                break
        
        # Determine if human handoff is needed
        requires_handoff = (
            sentiment_score < -0.5 or 
            intent_classification in ['complaint', 'support_request'] or
            'speak to human' in content_lower or
            'manager' in content_lower
        )
        
        handoff_reason = None
        if requires_handoff:
            if sentiment_score < -0.5:
                handoff_reason = 'Negative sentiment detected'
            elif intent_classification == 'complaint':
                handoff_reason = 'Customer complaint requires human attention'
            elif 'speak to human' in content_lower:
                handoff_reason = 'Customer requested human agent'
        
        # Save analysis
        ai_conversation = AIConversation(
            contact_id=contact_id,
            conversation_id=conversation_id,
            sentiment_score=sentiment_score,
            intent_classification=intent_classification,
            confidence_score=confidence_score,
            requires_human_handoff=requires_handoff,
            handoff_reason=handoff_reason,
            context=json.dumps({
                'message_length': len(message_content),
                'analysis_timestamp': datetime.utcnow().isoformat()
            })
        )
        
        db.session.add(ai_conversation)
        db.session.commit()
        
        return jsonify({
            'sentiment_score': sentiment_score,
            'sentiment_label': 'positive' if sentiment_score > 0.2 else 'negative' if sentiment_score < -0.2 else 'neutral',
            'intent_classification': intent_classification,
            'confidence_score': confidence_score,
            'requires_human_handoff': requires_handoff,
            'handoff_reason': handoff_reason,
            'suggested_response': 'Thank you for your message. How can I help you today?' if sentiment_score >= 0 else 'I understand your concern. Let me connect you with a specialist who can help.'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

