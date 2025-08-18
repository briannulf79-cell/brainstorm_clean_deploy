from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.contact import Contact, ContactActivity, ContactNote, ContactTask
from src.models.agency import SubAccount
from datetime import datetime
import json

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('', methods=['GET'])
def get_contacts():
    try:
        # Get query parameters
        sub_account_id = request.args.get('sub_account_id', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        tags = request.args.get('tags', '')
        status = request.args.get('status', '')
        
        # Build query
        query = Contact.query
        
        if sub_account_id:
            query = query.filter_by(sub_account_id=sub_account_id)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    Contact.first_name.ilike(search_term),
                    Contact.last_name.ilike(search_term),
                    Contact.email.ilike(search_term),
                    Contact.company.ilike(search_term)
                )
            )
        
        if status:
            query = query.filter_by(status=status)
        
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                query = query.filter(Contact.tags.contains(tag.strip()))
        
        # Paginate results
        contacts = query.order_by(Contact.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'contacts': [contact.to_dict() for contact in contacts.items],
            'total': contacts.total,
            'pages': contacts.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contacts_bp.route('', methods=['POST'])
def create_contact():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('sub_account_id'):
            return jsonify({'error': 'sub_account_id is required'}), 400
        
        # Create contact
        contact = Contact(
            sub_account_id=data.get('sub_account_id'),
            email=data.get('email'),
            phone=data.get('phone'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            company=data.get('company'),
            tags=json.dumps(data.get('tags', [])),
            custom_fields=json.dumps(data.get('custom_fields', {})),
            source=data.get('source'),
            status=data.get('status', 'active')
        )
        
        db.session.add(contact)
        db.session.commit()
        
        # Create activity record
        activity = ContactActivity(
            contact_id=contact.id,
            type='created',
            description='Contact created'
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Contact created successfully',
            'contact': contact.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@contacts_bp.route('/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        
        # Get recent activities
        activities = ContactActivity.query.filter_by(contact_id=contact_id)\
            .order_by(ContactActivity.created_at.desc()).limit(10).all()
        
        # Get notes
        notes = ContactNote.query.filter_by(contact_id=contact_id)\
            .order_by(ContactNote.created_at.desc()).all()
        
        # Get tasks
        tasks = ContactTask.query.filter_by(contact_id=contact_id)\
            .order_by(ContactTask.created_at.desc()).all()
        
        contact_data = contact.to_dict()
        contact_data['activities'] = [activity.to_dict() for activity in activities]
        contact_data['notes'] = [note.to_dict() for note in notes]
        contact_data['tasks'] = [task.to_dict() for task in tasks]
        
        return jsonify({'contact': contact_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contacts_bp.route('/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        data = request.get_json()
        
        # Update fields
        if 'email' in data:
            contact.email = data['email']
        if 'phone' in data:
            contact.phone = data['phone']
        if 'first_name' in data:
            contact.first_name = data['first_name']
        if 'last_name' in data:
            contact.last_name = data['last_name']
        if 'company' in data:
            contact.company = data['company']
        if 'tags' in data:
            contact.tags = json.dumps(data['tags'])
        if 'custom_fields' in data:
            contact.custom_fields = json.dumps(data['custom_fields'])
        if 'status' in data:
            contact.status = data['status']
        if 'source' in data:
            contact.source = data['source']
        
        contact.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Create activity record
        activity = ContactActivity(
            contact_id=contact.id,
            type='updated',
            description='Contact updated'
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Contact updated successfully',
            'contact': contact.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@contacts_bp.route('/<int:contact_id>/notes', methods=['POST'])
def add_contact_note(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        data = request.get_json()
        
        if not data.get('content'):
            return jsonify({'error': 'Note content is required'}), 400
        
        note = ContactNote(
            contact_id=contact_id,
            user_id=data.get('user_id'),  # Should come from auth token
            content=data['content'],
            is_private=data.get('is_private', False)
        )
        
        db.session.add(note)
        db.session.commit()
        
        # Create activity record
        activity = ContactActivity(
            contact_id=contact_id,
            type='note_added',
            description='Note added to contact'
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Note added successfully',
            'note': note.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@contacts_bp.route('/<int:contact_id>/tasks', methods=['POST'])
def add_contact_task(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'error': 'Task title is required'}), 400
        
        task = ContactTask(
            contact_id=contact_id,
            user_id=data.get('user_id'),  # Should come from auth token
            title=data['title'],
            description=data.get('description'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            priority=data.get('priority', 'medium')
        )
        
        db.session.add(task)
        db.session.commit()
        
        # Create activity record
        activity = ContactActivity(
            contact_id=contact_id,
            type='task_created',
            description=f'Task created: {task.title}'
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Task created successfully',
            'task': task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

