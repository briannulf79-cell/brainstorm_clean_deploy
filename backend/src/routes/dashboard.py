from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.contact import Contact, ContactActivity
from src.models.pipeline import Opportunity
from src.models.campaign import Campaign
from src.models.agency import SubAccount
from datetime import datetime, timedelta
from sqlalchemy import func, and_

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/metrics', methods=['GET'])
def get_dashboard_metrics():
    try:
        sub_account_id = request.args.get('sub_account_id', type=int)
        days = request.args.get('days', 30, type=int)
        
        # Date range for metrics
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Base queries
        contact_query = Contact.query
        opportunity_query = Opportunity.query.join(Contact)
        campaign_query = Campaign.query
        
        if sub_account_id:
            contact_query = contact_query.filter_by(sub_account_id=sub_account_id)
            opportunity_query = opportunity_query.filter(Contact.sub_account_id == sub_account_id)
            campaign_query = campaign_query.filter_by(sub_account_id=sub_account_id)
        
        # Total contacts
        total_contacts = contact_query.count()
        
        # New contacts this period
        new_contacts = contact_query.filter(
            Contact.created_at >= start_date
        ).count()
        
        # Active campaigns
        active_campaigns = campaign_query.filter_by(status='active').count()
        
        # Total revenue (closed won opportunities)
        total_revenue = db.session.query(func.sum(Opportunity.value)).filter(
            and_(
                Opportunity.status == 'won',
                Opportunity.closed_at >= start_date
            )
        ).scalar() or 0
        
        # Conversion rate (opportunities won vs total)
        total_opportunities = opportunity_query.count()
        won_opportunities = opportunity_query.filter_by(status='won').count()
        conversion_rate = (won_opportunities / total_opportunities * 100) if total_opportunities > 0 else 0
        
        # Average deal size
        avg_deal_size = db.session.query(func.avg(Opportunity.value)).filter(
            Opportunity.status == 'won'
        ).scalar() or 0
        
        # Recent activities
        recent_activities = ContactActivity.query.join(Contact)
        if sub_account_id:
            recent_activities = recent_activities.filter(Contact.sub_account_id == sub_account_id)
        
        recent_activities = recent_activities.order_by(
            ContactActivity.created_at.desc()
        ).limit(10).all()
        
        return jsonify({
            'metrics': {
                'total_contacts': total_contacts,
                'new_contacts': new_contacts,
                'active_campaigns': active_campaigns,
                'total_revenue': float(total_revenue),
                'conversion_rate': round(conversion_rate, 1),
                'average_deal_size': float(avg_deal_size)
            },
            'recent_activities': [activity.to_dict() for activity in recent_activities]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/pipeline-overview', methods=['GET'])
def get_pipeline_overview():
    try:
        sub_account_id = request.args.get('sub_account_id', type=int)
        
        # Get opportunities by stage
        query = db.session.query(
            Opportunity.stage,
            func.count(Opportunity.id).label('count'),
            func.sum(Opportunity.value).label('total_value')
        ).join(Contact)
        
        if sub_account_id:
            query = query.filter(Contact.sub_account_id == sub_account_id)
        
        pipeline_data = query.filter(
            Opportunity.status == 'open'
        ).group_by(Opportunity.stage).all()
        
        stages = []
        for stage, count, total_value in pipeline_data:
            stages.append({
                'stage': stage,
                'count': count,
                'total_value': float(total_value or 0)
            })
        
        return jsonify({'pipeline_overview': stages})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/leads-over-time', methods=['GET'])
def get_leads_over_time():
    try:
        sub_account_id = request.args.get('sub_account_id', type=int)
        days = request.args.get('days', 30, type=int)
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get daily lead counts
        query = db.session.query(
            func.date(Contact.created_at).label('date'),
            func.count(Contact.id).label('count')
        )
        
        if sub_account_id:
            query = query.filter_by(sub_account_id=sub_account_id)
        
        daily_leads = query.filter(
            Contact.created_at >= start_date
        ).group_by(func.date(Contact.created_at)).all()
        
        # Format data for chart
        leads_data = []
        for date, count in daily_leads:
            leads_data.append({
                'date': date.isoformat(),
                'count': count
            })
        
        return jsonify({'leads_over_time': leads_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/campaign-performance', methods=['GET'])
def get_campaign_performance():
    try:
        sub_account_id = request.args.get('sub_account_id', type=int)
        
        query = Campaign.query
        if sub_account_id:
            query = query.filter_by(sub_account_id=sub_account_id)
        
        campaigns = query.filter(
            Campaign.status.in_(['active', 'completed'])
        ).limit(10).all()
        
        campaign_data = []
        for campaign in campaigns:
            # Mock performance data - in real implementation, 
            # this would come from actual tracking
            campaign_data.append({
                'name': campaign.name,
                'type': campaign.type,
                'status': campaign.status,
                'impressions': 25000,  # Mock data
                'clicks': 2500,        # Mock data
                'conversions': 125,    # Mock data
                'cost': 1500.00       # Mock data
            })
        
        return jsonify({'campaign_performance': campaign_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/upcoming-tasks', methods=['GET'])
def get_upcoming_tasks():
    try:
        sub_account_id = request.args.get('sub_account_id', type=int)
        
        from src.models.contact import ContactTask
        
        query = ContactTask.query.join(Contact)
        if sub_account_id:
            query = query.filter(Contact.sub_account_id == sub_account_id)
        
        upcoming_tasks = query.filter(
            and_(
                ContactTask.status == 'pending',
                ContactTask.due_date >= datetime.utcnow()
            )
        ).order_by(ContactTask.due_date.asc()).limit(10).all()
        
        return jsonify({
            'upcoming_tasks': [task.to_dict() for task in upcoming_tasks]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

