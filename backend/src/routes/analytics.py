from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.user import db
from src.models.contact import Contact
from src.models.pipeline import Pipeline, Opportunity
from src.models.campaign import Campaign
import json
import random

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/overview', methods=['GET'])
def get_analytics_overview():
    """Get analytics overview with key metrics"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        timeframe = request.args.get('timeframe', '30d')
        
        # Calculate date range
        if timeframe == '7d':
            start_date = datetime.utcnow() - timedelta(days=7)
        elif timeframe == '30d':
            start_date = datetime.utcnow() - timedelta(days=30)
        elif timeframe == '90d':
            start_date = datetime.utcnow() - timedelta(days=90)
        elif timeframe == '1y':
            start_date = datetime.utcnow() - timedelta(days=365)
        else:
            start_date = datetime.utcnow() - timedelta(days=30)
        
        # Get basic counts
        total_contacts = Contact.query.filter_by(sub_account_id=sub_account_id).count()
        new_contacts = Contact.query.filter(
            Contact.sub_account_id == sub_account_id,
            Contact.created_at >= start_date
        ).count()
        
        # Mock revenue data - in production, this would come from actual deals/orders
        total_revenue = 125000 + (random.randint(-10000, 20000))
        revenue_growth = random.uniform(5.0, 25.0)
        conversion_rate = random.uniform(2.0, 8.0)
        conversion_change = random.uniform(-1.0, 3.0)
        avg_deal_size = random.randint(3000, 6000)
        deal_size_change = random.uniform(-5.0, 5.0)
        
        overview = {
            'total_contacts': total_contacts,
            'new_contacts': new_contacts,
            'total_revenue': total_revenue,
            'revenue_growth': revenue_growth,
            'conversion_rate': conversion_rate,
            'conversion_change': conversion_change,
            'avg_deal_size': avg_deal_size,
            'deal_size_change': deal_size_change,
            'timeframe': timeframe
        }
        
        return jsonify(overview)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/revenue-trend', methods=['GET'])
def get_revenue_trend():
    """Get revenue trend data over time"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        timeframe = request.args.get('timeframe', '30d')
        
        # Generate mock revenue trend data
        if timeframe == '7d':
            days = 7
        elif timeframe == '30d':
            days = 30
        elif timeframe == '90d':
            days = 90
        else:
            days = 30
        
        trend_data = []
        base_revenue = 3000
        
        for i in range(days):
            date = (datetime.utcnow() - timedelta(days=days-i-1)).strftime('%Y-%m-%d')
            # Add some randomness and trend
            daily_revenue = base_revenue + random.randint(-1000, 2000) + (i * 50)
            deals = random.randint(1, 8)
            
            trend_data.append({
                'date': date,
                'revenue': max(0, daily_revenue),
                'deals': deals
            })
        
        return jsonify({
            'trend_data': trend_data,
            'timeframe': timeframe
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/lead-sources', methods=['GET'])
def get_lead_sources():
    """Get lead source distribution"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        
        # Mock lead source data - in production, analyze actual contact sources
        lead_sources = [
            {'name': 'Website', 'value': 35, 'count': 998, 'color': '#3b82f6'},
            {'name': 'Referrals', 'value': 25, 'count': 712, 'color': '#10b981'},
            {'name': 'Social Media', 'value': 20, 'count': 569, 'color': '#f59e0b'},
            {'name': 'Google Ads', 'value': 15, 'count': 427, 'color': '#ef4444'},
            {'name': 'Other', 'value': 5, 'count': 141, 'color': '#8b5cf6'}
        ]
        
        return jsonify({
            'lead_sources': lead_sources,
            'total_leads': sum(source['count'] for source in lead_sources)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/campaign-performance', methods=['GET'])
def get_campaign_performance():
    """Get campaign performance metrics"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        
        # Mock campaign performance data
        campaigns = [
            {
                'name': 'Summer Sale 2024',
                'type': 'email',
                'sent': 2500,
                'opened': 625,
                'clicked': 125,
                'converted': 25,
                'revenue': 12500,
                'cost': 500,
                'status': 'completed'
            },
            {
                'name': 'Product Demo Series',
                'type': 'email',
                'sent': 1800,
                'opened': 540,
                'clicked': 108,
                'converted': 18,
                'revenue': 9000,
                'cost': 300,
                'status': 'active'
            },
            {
                'name': 'LinkedIn Outreach',
                'type': 'social',
                'sent': 3200,
                'opened': 960,
                'clicked': 192,
                'converted': 32,
                'revenue': 16000,
                'cost': 800,
                'status': 'completed'
            },
            {
                'name': 'Webinar Promotion',
                'type': 'email',
                'sent': 1200,
                'opened': 360,
                'clicked': 72,
                'converted': 12,
                'revenue': 6000,
                'cost': 200,
                'status': 'active'
            }
        ]
        
        # Calculate additional metrics
        for campaign in campaigns:
            campaign['open_rate'] = (campaign['opened'] / campaign['sent']) * 100 if campaign['sent'] > 0 else 0
            campaign['click_rate'] = (campaign['clicked'] / campaign['opened']) * 100 if campaign['opened'] > 0 else 0
            campaign['conversion_rate'] = (campaign['converted'] / campaign['clicked']) * 100 if campaign['clicked'] > 0 else 0
            campaign['roi'] = ((campaign['revenue'] - campaign['cost']) / campaign['cost']) * 100 if campaign['cost'] > 0 else 0
        
        return jsonify({
            'campaigns': campaigns,
            'total_campaigns': len(campaigns)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/pipeline-conversion', methods=['GET'])
def get_pipeline_conversion():
    """Get pipeline conversion funnel data"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        
        # Mock pipeline conversion data
        pipeline_stages = [
            {'stage': 'Lead', 'count': 1000, 'converted': 600, 'conversion_rate': 60.0},
            {'stage': 'Qualified', 'count': 600, 'converted': 300, 'conversion_rate': 50.0},
            {'stage': 'Proposal', 'count': 300, 'converted': 150, 'conversion_rate': 50.0},
            {'stage': 'Negotiation', 'count': 150, 'converted': 90, 'conversion_rate': 60.0},
            {'stage': 'Closed Won', 'count': 90, 'converted': 90, 'conversion_rate': 100.0}
        ]
        
        return jsonify({
            'pipeline_stages': pipeline_stages,
            'overall_conversion': (90 / 1000) * 100  # 9% overall conversion
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/channel-performance', methods=['GET'])
def get_channel_performance():
    """Get performance metrics by channel"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        
        # Mock channel performance data
        channels = [
            {
                'channel': 'Email',
                'leads': 456,
                'conversions': 107,
                'revenue': 45000,
                'cost': 2500,
                'avg_deal_size': 420,
                'conversion_rate': 23.5,
                'roi': 1700,
                'trend': 'up'
            },
            {
                'channel': 'Social Media',
                'leads': 324,
                'conversions': 68,
                'revenue': 28500,
                'cost': 3200,
                'avg_deal_size': 419,
                'conversion_rate': 21.0,
                'roi': 791,
                'trend': 'up'
            },
            {
                'channel': 'Paid Ads',
                'leads': 289,
                'conversions': 72,
                'revenue': 32000,
                'cost': 8500,
                'avg_deal_size': 444,
                'conversion_rate': 24.9,
                'roi': 276,
                'trend': 'stable'
            },
            {
                'channel': 'Organic Search',
                'leads': 178,
                'conversions': 46,
                'revenue': 19500,
                'cost': 0,
                'avg_deal_size': 424,
                'conversion_rate': 25.8,
                'roi': float('inf'),
                'trend': 'up'
            },
            {
                'channel': 'Referrals',
                'leads': 145,
                'conversions': 42,
                'revenue': 18900,
                'cost': 500,
                'avg_deal_size': 450,
                'conversion_rate': 29.0,
                'roi': 3680,
                'trend': 'up'
            }
        ]
        
        return jsonify({
            'channels': channels,
            'total_leads': sum(ch['leads'] for ch in channels),
            'total_conversions': sum(ch['conversions'] for ch in channels),
            'total_revenue': sum(ch['revenue'] for ch in channels)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/time-series', methods=['GET'])
def get_time_series_data():
    """Get time series data for detailed analysis"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        timeframe = request.args.get('timeframe', '30d')
        metric = request.args.get('metric', 'all')  # all, revenue, leads, conversions
        
        # Generate time series data
        if timeframe == '7d':
            days = 7
        elif timeframe == '30d':
            days = 30
        elif timeframe == '90d':
            days = 90
        else:
            days = 30
        
        time_series = []
        for i in range(days):
            date = (datetime.utcnow() - timedelta(days=days-i-1)).strftime('%Y-%m-%d')
            
            # Generate realistic data with trends and seasonality
            base_visitors = 400 + random.randint(-100, 200)
            visitors = max(100, base_visitors + (i * 2))  # Slight upward trend
            
            leads = max(10, int(visitors * random.uniform(0.08, 0.15)))
            conversions = max(1, int(leads * random.uniform(0.15, 0.35)))
            revenue = conversions * random.randint(300, 800)
            
            time_series.append({
                'date': date,
                'visitors': visitors,
                'leads': leads,
                'conversions': conversions,
                'revenue': revenue,
                'conversion_rate': (conversions / leads) * 100 if leads > 0 else 0,
                'avg_deal_size': revenue / conversions if conversions > 0 else 0
            })
        
        return jsonify({
            'time_series': time_series,
            'timeframe': timeframe,
            'metric': metric
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/ai-insights', methods=['GET'])
def get_ai_insights():
    """Get AI-powered business insights"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        
        # Mock AI insights - in production, these would be generated by ML models
        insights = [
            {
                'type': 'performance',
                'category': 'conversion',
                'title': 'Strong Performance Detected',
                'description': 'Your conversion rate is 23% above industry average. Website leads are performing exceptionally well.',
                'impact': 'positive',
                'confidence': 87,
                'recommendation': 'Continue current website optimization strategies and consider increasing ad spend for website traffic.',
                'metrics': {
                    'current_rate': 3.2,
                    'industry_average': 2.6,
                    'improvement': 23.1
                }
            },
            {
                'type': 'opportunity',
                'category': 'channel_optimization',
                'title': 'Social Media Optimization Opportunity',
                'description': 'Social media campaigns have lower conversion rates compared to other channels.',
                'impact': 'neutral',
                'confidence': 73,
                'recommendation': 'Consider A/B testing different messaging approaches and targeting parameters for social media campaigns.',
                'metrics': {
                    'current_rate': 2.1,
                    'potential_rate': 2.8,
                    'potential_revenue_increase': 8500
                }
            },
            {
                'type': 'prediction',
                'category': 'revenue_forecast',
                'title': 'Revenue Growth Prediction',
                'description': 'Based on current trends, revenue is projected to increase by 15% next month.',
                'impact': 'positive',
                'confidence': 82,
                'recommendation': 'Prepare for increased demand and consider scaling customer support resources.',
                'metrics': {
                    'current_monthly': 125000,
                    'predicted_monthly': 143750,
                    'growth_rate': 15.0
                }
            },
            {
                'type': 'alert',
                'category': 'churn_risk',
                'title': 'Potential Churn Risk',
                'description': '12 high-value customers show decreased engagement patterns similar to churned customers.',
                'impact': 'negative',
                'confidence': 91,
                'recommendation': 'Implement immediate re-engagement campaigns for at-risk customers.',
                'metrics': {
                    'at_risk_customers': 12,
                    'potential_revenue_loss': 54000,
                    'recommended_action': 'urgent'
                }
            }
        ]
        
        return jsonify({
            'insights': insights,
            'total_insights': len(insights),
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/export', methods=['POST'])
def export_analytics():
    """Export analytics data in various formats"""
    try:
        data = request.get_json()
        
        export_format = data.get('format', 'csv')  # csv, pdf, excel
        report_type = data.get('report_type', 'overview')  # overview, detailed, custom
        date_range = data.get('date_range', '30d')
        sub_account_id = data.get('sub_account_id', 1)
        
        # Mock export functionality - in production, generate actual files
        export_data = {
            'export_id': f"export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'format': export_format,
            'report_type': report_type,
            'date_range': date_range,
            'status': 'processing',
            'estimated_completion': (datetime.utcnow() + timedelta(minutes=2)).isoformat(),
            'download_url': None  # Will be populated when ready
        }
        
        return jsonify({
            'message': 'Export initiated successfully',
            'export_data': export_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/custom-report', methods=['POST'])
def create_custom_report():
    """Create a custom analytics report"""
    try:
        data = request.get_json()
        
        report_config = {
            'name': data.get('name', 'Custom Report'),
            'metrics': data.get('metrics', []),
            'filters': data.get('filters', {}),
            'date_range': data.get('date_range', '30d'),
            'visualization_type': data.get('visualization_type', 'chart'),
            'schedule': data.get('schedule', None)  # For automated reports
        }
        
        # Mock report creation
        report = {
            'id': f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'config': report_config,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'created',
            'url': f"/analytics/reports/{report_config['name'].lower().replace(' ', '_')}"
        }
        
        return jsonify({
            'message': 'Custom report created successfully',
            'report': report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

