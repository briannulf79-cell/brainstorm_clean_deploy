from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.pipeline import Pipeline, Opportunity, OpportunityActivity
from src.models.contact import Contact
from datetime import datetime
import json

pipelines_bp = Blueprint('pipelines', __name__)

@pipelines_bp.route('', methods=['GET'])
def get_pipelines():
    try:
        sub_account_id = request.args.get('sub_account_id', type=int)
        
        query = Pipeline.query
        if sub_account_id:
            query = query.filter_by(sub_account_id=sub_account_id)
        
        pipelines = query.order_by(Pipeline.created_at.desc()).all()
        
        return jsonify({
            'pipelines': [pipeline.to_dict() for pipeline in pipelines]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pipelines_bp.route('', methods=['POST'])
def create_pipeline():
    try:
        data = request.get_json()
        
        if not data.get('sub_account_id') or not data.get('name'):
            return jsonify({'error': 'sub_account_id and name are required'}), 400
        
        # Default stages if not provided
        default_stages = [
            {'name': 'Lead', 'order': 0, 'color': '#3b82f6'},
            {'name': 'Qualified', 'order': 1, 'color': '#10b981'},
            {'name': 'Proposal', 'order': 2, 'color': '#f59e0b'},
            {'name': 'Negotiation', 'order': 3, 'color': '#ef4444'},
            {'name': 'Closed Won', 'order': 4, 'color': '#22c55e'}
        ]
        
        pipeline = Pipeline(
            sub_account_id=data['sub_account_id'],
            name=data['name'],
            stages=json.dumps(data.get('stages', default_stages)),
            settings=json.dumps(data.get('settings', {})),
            is_default=data.get('is_default', False)
        )
        
        db.session.add(pipeline)
        db.session.commit()
        
        return jsonify({
            'message': 'Pipeline created successfully',
            'pipeline': pipeline.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pipelines_bp.route('/<int:pipeline_id>/opportunities', methods=['GET'])
def get_pipeline_opportunities(pipeline_id):
    try:
        pipeline = Pipeline.query.get_or_404(pipeline_id)
        
        opportunities = Opportunity.query.filter_by(pipeline_id=pipeline_id)\
            .order_by(Opportunity.created_at.desc()).all()
        
        # Group opportunities by stage
        stages_data = {}
        stages = json.loads(pipeline.stages) if pipeline.stages else []
        
        for stage in stages:
            stage_name = stage['name']
            stage_opportunities = [
                opp.to_dict() for opp in opportunities 
                if opp.stage == stage_name
            ]
            stages_data[stage_name] = {
                'stage_info': stage,
                'opportunities': stage_opportunities,
                'count': len(stage_opportunities),
                'total_value': sum(opp.value or 0 for opp in opportunities if opp.stage == stage_name)
            }
        
        return jsonify({
            'pipeline': pipeline.to_dict(),
            'stages': stages_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pipelines_bp.route('/opportunities', methods=['POST'])
def create_opportunity():
    try:
        data = request.get_json()
        
        required_fields = ['pipeline_id', 'contact_id', 'title', 'stage']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Verify contact exists
        contact = Contact.query.get(data['contact_id'])
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404
        
        opportunity = Opportunity(
            pipeline_id=data['pipeline_id'],
            contact_id=data['contact_id'],
            user_id=data.get('user_id'),
            title=data['title'],
            description=data.get('description'),
            stage=data['stage'],
            value=data.get('value', 0),
            probability=data.get('probability', 0),
            expected_close_date=datetime.fromisoformat(data['expected_close_date']) if data.get('expected_close_date') else None,
            source=data.get('source'),
            custom_fields=json.dumps(data.get('custom_fields', {}))
        )
        
        db.session.add(opportunity)
        db.session.commit()
        
        # Create activity record
        activity = OpportunityActivity(
            opportunity_id=opportunity.id,
            type='created',
            description='Opportunity created',
            new_value=opportunity.stage
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Opportunity created successfully',
            'opportunity': opportunity.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pipelines_bp.route('/opportunities/<int:opportunity_id>/stage', methods=['PUT'])
def update_opportunity_stage(opportunity_id):
    try:
        opportunity = Opportunity.query.get_or_404(opportunity_id)
        data = request.get_json()
        
        if not data.get('stage'):
            return jsonify({'error': 'stage is required'}), 400
        
        old_stage = opportunity.stage
        new_stage = data['stage']
        
        opportunity.stage = new_stage
        opportunity.updated_at = datetime.utcnow()
        
        # Update probability based on stage if provided
        if 'probability' in data:
            opportunity.probability = data['probability']
        
        db.session.commit()
        
        # Create activity record
        activity = OpportunityActivity(
            opportunity_id=opportunity_id,
            type='stage_change',
            description=f'Stage changed from {old_stage} to {new_stage}',
            old_value=old_stage,
            new_value=new_stage
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Opportunity stage updated successfully',
            'opportunity': opportunity.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pipelines_bp.route('/opportunities/<int:opportunity_id>', methods=['PUT'])
def update_opportunity(opportunity_id):
    try:
        opportunity = Opportunity.query.get_or_404(opportunity_id)
        data = request.get_json()
        
        # Track changes for activity log
        changes = []
        
        if 'title' in data and data['title'] != opportunity.title:
            changes.append(f"Title changed from '{opportunity.title}' to '{data['title']}'")
            opportunity.title = data['title']
        
        if 'description' in data:
            opportunity.description = data['description']
        
        if 'value' in data and data['value'] != opportunity.value:
            changes.append(f"Value changed from {opportunity.value} to {data['value']}")
            opportunity.value = data['value']
        
        if 'probability' in data and data['probability'] != opportunity.probability:
            changes.append(f"Probability changed from {opportunity.probability}% to {data['probability']}%")
            opportunity.probability = data['probability']
        
        if 'expected_close_date' in data:
            new_date = datetime.fromisoformat(data['expected_close_date']) if data['expected_close_date'] else None
            if new_date != opportunity.expected_close_date:
                changes.append(f"Expected close date changed")
                opportunity.expected_close_date = new_date
        
        if 'custom_fields' in data:
            opportunity.custom_fields = json.dumps(data['custom_fields'])
        
        opportunity.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Create activity record if there were changes
        if changes:
            activity = OpportunityActivity(
                opportunity_id=opportunity_id,
                type='updated',
                description='; '.join(changes)
            )
            db.session.add(activity)
            db.session.commit()
        
        return jsonify({
            'message': 'Opportunity updated successfully',
            'opportunity': opportunity.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

