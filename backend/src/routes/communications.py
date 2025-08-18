from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import desc, or_, and_
from src.models.user import db
from src.models.communications import (
    Conversation, Message, EmailAccount, SMSAccount, CallAccount,
    MessageType, MessageDirection, ConversationStatus, MessageStatus
)
from src.models.contact import Contact
from src.models.user import User

communications_bp = Blueprint('communications', __name__)

@communications_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations for a sub-account"""
    try:
        # Get query parameters
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        message_type = request.args.get('type')
        search = request.args.get('search')
        assigned_to = request.args.get('assigned_to', type=int)
        
        # Build query
        query = Conversation.query.filter_by(sub_account_id=sub_account_id)
        
        # Apply filters
        if status:
            query = query.filter(Conversation.status == ConversationStatus(status))
        
        if message_type:
            query = query.filter(Conversation.type == MessageType(message_type))
        
        if assigned_to:
            query = query.filter(Conversation.assigned_to_id == assigned_to)
        
        if search:
            query = query.join(Contact).filter(
                or_(
                    Contact.first_name.ilike(f'%{search}%'),
                    Contact.last_name.ilike(f'%{search}%'),
                    Contact.email.ilike(f'%{search}%'),
                    Conversation.subject.ilike(f'%{search}%')
                )
            )
        
        # Order by last message time
        query = query.order_by(desc(Conversation.last_message_at))
        
        # Paginate
        conversations = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'conversations': [conv.to_dict() for conv in conversations.items],
            'total': conversations.total,
            'pages': conversations.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['sub_account_id', 'contact_id', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create conversation
        conversation = Conversation(
            sub_account_id=data['sub_account_id'],
            contact_id=data['contact_id'],
            type=MessageType(data['type']),
            subject=data.get('subject'),
            assigned_to_id=data.get('assigned_to_id'),
            status=ConversationStatus(data.get('status', 'open')),
            tags=data.get('tags', []),
            custom_fields=data.get('custom_fields', {})
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        return jsonify(conversation.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get a specific conversation with messages"""
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        
        # Get messages
        messages = Message.query.filter_by(conversation_id=conversation_id)\
            .order_by(Message.created_at).all()
        
        result = conversation.to_dict()
        result['messages'] = [msg.to_dict() for msg in messages]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/conversations/<int:conversation_id>', methods=['PUT'])
def update_conversation(conversation_id):
    """Update a conversation"""
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        data = request.get_json()
        
        # Update fields
        if 'status' in data:
            conversation.status = ConversationStatus(data['status'])
        if 'assigned_to_id' in data:
            conversation.assigned_to_id = data['assigned_to_id']
        if 'subject' in data:
            conversation.subject = data['subject']
        if 'tags' in data:
            conversation.tags = data['tags']
        if 'custom_fields' in data:
            conversation.custom_fields = data['custom_fields']
        
        conversation.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(conversation.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
def send_message():
    """Send a new message in a conversation"""
    try:
        conversation_id = request.view_args['conversation_id']
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content', 'direction']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get conversation
        conversation = Conversation.query.get_or_404(conversation_id)
        
        # Create message
        message = Message(
            conversation_id=conversation_id,
            type=conversation.type,
            direction=MessageDirection(data['direction']),
            content=data['content'],
            subject=data.get('subject'),
            from_address=data.get('from_address'),
            to_address=data.get('to_address'),
            from_name=data.get('from_name'),
            to_name=data.get('to_name'),
            html_content=data.get('html_content'),
            attachments=data.get('attachments', []),
            custom_fields=data.get('custom_fields', {})
        )
        
        # Set status based on direction
        if data['direction'] == 'outbound':
            message.status = MessageStatus.SENT
            message.sent_at = datetime.utcnow()
        else:
            message.status = MessageStatus.DELIVERED
            message.delivered_at = datetime.utcnow()
        
        db.session.add(message)
        
        # Update conversation
        conversation.last_message_at = datetime.utcnow()
        conversation.message_count = (conversation.message_count or 0) + 1
        
        if data['direction'] == 'inbound':
            conversation.unread_count = (conversation.unread_count or 0) + 1
        
        # AI Analysis (mock for demo)
        if data['direction'] == 'inbound':
            message.ai_sentiment = analyze_sentiment(data['content'])
            message.ai_intent = analyze_intent(data['content'])
            conversation.ai_sentiment = message.ai_sentiment
            conversation.ai_priority = determine_priority(data['content'])
        
        db.session.commit()
        
        # In a real implementation, you would:
        # 1. Send the actual email/SMS/make call
        # 2. Update message status based on delivery
        # 3. Handle webhooks for delivery confirmations
        
        return jsonify(message.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/conversations/<int:conversation_id>/mark-read', methods=['POST'])
def mark_conversation_read(conversation_id):
    """Mark all messages in a conversation as read"""
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        
        # Update unread messages
        Message.query.filter_by(conversation_id=conversation_id)\
            .filter(Message.direction == MessageDirection.INBOUND)\
            .filter(Message.read_at.is_(None))\
            .update({'read_at': datetime.utcnow()})
        
        # Reset unread count
        conversation.unread_count = 0
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/email-accounts', methods=['GET'])
def get_email_accounts():
    """Get all email accounts for a sub-account"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        
        accounts = EmailAccount.query.filter_by(sub_account_id=sub_account_id).all()
        
        return jsonify([account.to_dict() for account in accounts])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/email-accounts', methods=['POST'])
def create_email_account():
    """Create a new email account"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['sub_account_id', 'user_id', 'email_address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create email account
        account = EmailAccount(
            sub_account_id=data['sub_account_id'],
            user_id=data['user_id'],
            email_address=data['email_address'],
            display_name=data.get('display_name'),
            smtp_host=data.get('smtp_host'),
            smtp_port=data.get('smtp_port'),
            smtp_username=data.get('smtp_username'),
            smtp_password=data.get('smtp_password'),  # Should be encrypted
            smtp_use_tls=data.get('smtp_use_tls', True),
            smtp_use_ssl=data.get('smtp_use_ssl', False),
            imap_host=data.get('imap_host'),
            imap_port=data.get('imap_port'),
            imap_username=data.get('imap_username'),
            imap_password=data.get('imap_password'),  # Should be encrypted
            imap_use_ssl=data.get('imap_use_ssl', True),
            oauth_provider=data.get('oauth_provider'),
            auto_sync=data.get('auto_sync', True),
            sync_frequency=data.get('sync_frequency', 5)
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify(account.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/sms-accounts', methods=['GET'])
def get_sms_accounts():
    """Get all SMS accounts for a sub-account"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        
        accounts = SMSAccount.query.filter_by(sub_account_id=sub_account_id).all()
        
        return jsonify([account.to_dict() for account in accounts])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/sms-accounts', methods=['POST'])
def create_sms_account():
    """Create a new SMS account"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['sub_account_id', 'phone_number', 'provider']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create SMS account
        account = SMSAccount(
            sub_account_id=data['sub_account_id'],
            phone_number=data['phone_number'],
            display_name=data.get('display_name'),
            provider=data['provider'],
            account_sid=data.get('account_sid'),
            auth_token=data.get('auth_token'),  # Should be encrypted
            api_key=data.get('api_key'),
            api_secret=data.get('api_secret'),  # Should be encrypted
            webhook_url=data.get('webhook_url')
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify(account.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/call-accounts', methods=['GET'])
def get_call_accounts():
    """Get all call accounts for a sub-account"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        
        accounts = CallAccount.query.filter_by(sub_account_id=sub_account_id).all()
        
        return jsonify([account.to_dict() for account in accounts])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/call-accounts', methods=['POST'])
def create_call_account():
    """Create a new call account"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['sub_account_id', 'phone_number', 'provider']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create call account
        account = CallAccount(
            sub_account_id=data['sub_account_id'],
            phone_number=data['phone_number'],
            display_name=data.get('display_name'),
            provider=data['provider'],
            account_sid=data.get('account_sid'),
            auth_token=data.get('auth_token'),  # Should be encrypted
            api_key=data.get('api_key'),
            api_secret=data.get('api_secret'),  # Should be encrypted
            recording_enabled=data.get('recording_enabled', True),
            transcription_enabled=data.get('transcription_enabled', True),
            voicemail_enabled=data.get('voicemail_enabled', True),
            call_forwarding_number=data.get('call_forwarding_number'),
            webhook_url=data.get('webhook_url')
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify(account.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@communications_bp.route('/stats', methods=['GET'])
def get_communication_stats():
    """Get communication statistics"""
    try:
        sub_account_id = request.args.get('sub_account_id', 1, type=int)
        days = request.args.get('days', 30, type=int)
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get conversation stats
        total_conversations = Conversation.query.filter_by(sub_account_id=sub_account_id).count()
        
        active_conversations = Conversation.query.filter_by(
            sub_account_id=sub_account_id,
            status=ConversationStatus.OPEN
        ).count()
        
        # Get message stats
        total_messages = Message.query.join(Conversation)\
            .filter(Conversation.sub_account_id == sub_account_id)\
            .filter(Message.created_at >= start_date).count()
        
        inbound_messages = Message.query.join(Conversation)\
            .filter(Conversation.sub_account_id == sub_account_id)\
            .filter(Message.direction == MessageDirection.INBOUND)\
            .filter(Message.created_at >= start_date).count()
        
        outbound_messages = Message.query.join(Conversation)\
            .filter(Conversation.sub_account_id == sub_account_id)\
            .filter(Message.direction == MessageDirection.OUTBOUND)\
            .filter(Message.created_at >= start_date).count()
        
        # Response time stats (mock for demo)
        avg_response_time = "2h 15m"
        
        # Channel breakdown
        email_conversations = Conversation.query.filter_by(
            sub_account_id=sub_account_id,
            type=MessageType.EMAIL
        ).count()
        
        sms_conversations = Conversation.query.filter_by(
            sub_account_id=sub_account_id,
            type=MessageType.SMS
        ).count()
        
        call_conversations = Conversation.query.filter_by(
            sub_account_id=sub_account_id,
            type=MessageType.CALL
        ).count()
        
        return jsonify({
            'total_conversations': total_conversations,
            'active_conversations': active_conversations,
            'total_messages': total_messages,
            'inbound_messages': inbound_messages,
            'outbound_messages': outbound_messages,
            'avg_response_time': avg_response_time,
            'channel_breakdown': {
                'email': email_conversations,
                'sms': sms_conversations,
                'call': call_conversations
            },
            'period_days': days
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AI Analysis Helper Functions (Mock implementations)
def analyze_sentiment(content):
    """Analyze message sentiment using AI"""
    # Mock implementation - in reality, you'd use OpenAI, AWS Comprehend, etc.
    positive_words = ['great', 'excellent', 'love', 'amazing', 'perfect', 'thank you']
    negative_words = ['bad', 'terrible', 'hate', 'awful', 'problem', 'issue']
    
    content_lower = content.lower()
    
    positive_count = sum(1 for word in positive_words if word in content_lower)
    negative_count = sum(1 for word in negative_words if word in content_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'

def analyze_intent(content):
    """Analyze message intent using AI"""
    # Mock implementation
    content_lower = content.lower()
    
    if any(word in content_lower for word in ['demo', 'demonstration', 'show me']):
        return 'demo_request'
    elif any(word in content_lower for word in ['price', 'cost', 'pricing', 'how much']):
        return 'pricing_inquiry'
    elif any(word in content_lower for word in ['help', 'support', 'problem', 'issue']):
        return 'support_request'
    elif any(word in content_lower for word in ['meeting', 'call', 'schedule']):
        return 'meeting_request'
    else:
        return 'general_inquiry'

def determine_priority(content):
    """Determine message priority using AI"""
    # Mock implementation
    content_lower = content.lower()
    
    high_priority_words = ['urgent', 'asap', 'immediately', 'emergency', 'critical']
    
    if any(word in content_lower for word in high_priority_words):
        return 'high'
    elif any(word in content_lower for word in ['demo', 'pricing', 'meeting']):
        return 'high'
    else:
        return 'medium'

