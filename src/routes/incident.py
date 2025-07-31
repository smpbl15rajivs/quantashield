from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import Incident, db

incident_bp = Blueprint('incident', __name__)

@incident_bp.route('/incidents', methods=['GET'])
@jwt_required()
def get_incidents():
    """Get all incidents with filtering and pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        status = request.args.get('status')
        severity = request.args.get('severity')
        assigned_to = request.args.get('assigned_to', type=int)
        
        query = Incident.query
        
        if status:
            query = query.filter(Incident.status == status)
        if severity:
            query = query.filter(Incident.severity == severity)
        if assigned_to:
            query = query.filter(Incident.assigned_to == assigned_to)
        
        # Order by creation date (newest first)
        query = query.order_by(Incident.created_at.desc())
        
        paginated = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'incidents': [incident.to_dict() for incident in paginated.items],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': paginated.total,
                    'pages': paginated.pages
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500

@incident_bp.route('/incidents', methods=['POST'])
@jwt_required()
def create_incident():
    """Create a new incident."""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Validate required fields
        required_fields = ['title', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': f'{field} is required'
                    }
                }), 400
        
        incident = Incident(
            title=data['title'],
            description=data['description'],
            severity=data.get('severity', 'medium'),
            category=data.get('category'),
            source=data.get('source'),
            assigned_to=data.get('assigned_to'),
            created_by=current_user_id
        )
        
        db.session.add(incident)
        db.session.commit()
        
        # Add initial timeline entry
        timeline_entry = IncidentTimeline(
            incident_id=incident.id,
            action='Incident Created',
            description=f'Incident created: {incident.title}',
            performed_by=current_user_id
        )
        db.session.add(timeline_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'incident': incident.to_dict()
            },
            'message': 'Incident created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500

@incident_bp.route('/incidents/<int:incident_id>', methods=['GET'])
@jwt_required()
def get_incident(incident_id):
    """Get a specific incident by ID."""
    try:
        incident = Incident.query.get_or_404(incident_id)
        return jsonify({
            'success': True,
            'data': {
                'incident': incident.to_dict()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500

@incident_bp.route('/incidents/<int:incident_id>', methods=['PUT'])
@jwt_required()
def update_incident(incident_id):
    """Update an incident."""
    try:
        incident = Incident.query.get_or_404(incident_id)
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Track changes for timeline
        changes = []
        
        updatable_fields = [
            'title', 'description', 'severity', 'status', 'category',
            'source', 'assigned_to'
        ]
        
        for field in updatable_fields:
            if field in data and getattr(incident, field) != data[field]:
                old_value = getattr(incident, field)
                new_value = data[field]
                setattr(incident, field, new_value)
                changes.append(f'{field.replace("_", " ").title()}: {old_value} → {new_value}')
        
        # Set resolved_at if status is resolved or closed
        if data.get('status') in ['resolved', 'closed'] and not incident.resolved_at:
            from datetime import datetime
            incident.resolved_at = datetime.utcnow()
            changes.append('Incident resolved')
        
        db.session.commit()
        
        # Add timeline entry for changes
        if changes:
            timeline_entry = IncidentTimeline(
                incident_id=incident.id,
                action='Incident Updated',
                description='; '.join(changes),
                performed_by=current_user_id
            )
            db.session.add(timeline_entry)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'incident': incident.to_dict()
            },
            'message': 'Incident updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500

@incident_bp.route('/incidents/<int:incident_id>/timeline', methods=['GET'])
@jwt_required()
def get_incident_timeline(incident_id):
    """Get timeline for a specific incident."""
    try:
        incident = Incident.query.get_or_404(incident_id)
        timeline = [entry.to_dict() for entry in incident.timeline]
        
        return jsonify({
            'success': True,
            'data': {
                'incident_id': incident_id,
                'timeline': timeline
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500

@incident_bp.route('/incidents/<int:incident_id>/timeline', methods=['POST'])
@jwt_required()
def add_timeline_entry(incident_id):
    """Add a timeline entry to an incident."""
    try:
        incident = Incident.query.get_or_404(incident_id)
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        if not data.get('action'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Action is required'
                }
            }), 400
        
        timeline_entry = IncidentTimeline(
            incident_id=incident_id,
            action=data['action'],
            description=data.get('description'),
            performed_by=current_user_id
        )
        
        db.session.add(timeline_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'timeline_entry': timeline_entry.to_dict()
            },
            'message': 'Timeline entry added successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500

