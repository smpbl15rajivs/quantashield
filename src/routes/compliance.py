from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import ComplianceFramework, Control, ControlAssessment, db

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/compliance/frameworks', methods=['GET'])
@jwt_required()
def get_compliance_frameworks():
    """Get all compliance frameworks."""
    try:
        frameworks = ComplianceFramework.query.filter_by(is_active=True).all()
        
        return jsonify({
            'success': True,
            'data': {
                'frameworks': [framework.to_dict() for framework in frameworks]
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

@compliance_bp.route('/compliance/frameworks', methods=['POST'])
@jwt_required()
def create_compliance_framework():
    """Create a new compliance framework."""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Name is required'
                }
            }), 400
        
        framework = ComplianceFramework(
            name=data['name'],
            version=data.get('version'),
            description=data.get('description')
        )
        
        db.session.add(framework)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'framework': framework.to_dict()
            },
            'message': 'Compliance framework created successfully'
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

@compliance_bp.route('/compliance/controls', methods=['GET'])
@jwt_required()
def get_controls():
    """Get controls with filtering."""
    try:
        framework_id = request.args.get('framework_id', type=int)
        category = request.args.get('category')
        
        query = Control.query
        
        if framework_id:
            query = query.filter(Control.framework_id == framework_id)
        if category:
            query = query.filter(Control.category == category)
        
        controls = query.all()
        
        return jsonify({
            'success': True,
            'data': {
                'controls': [control.to_dict() for control in controls]
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

@compliance_bp.route('/compliance/assessments', methods=['GET'])
@jwt_required()
def get_control_assessments():
    """Get control assessments with filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        framework_id = request.args.get('framework_id', type=int)
        status = request.args.get('status')
        
        query = ControlAssessment.query.join(Control)
        
        if framework_id:
            query = query.filter(Control.framework_id == framework_id)
        if status:
            query = query.filter(ControlAssessment.status == status)
        
        # Order by assessment date (newest first)
        query = query.order_by(ControlAssessment.assessment_date.desc())
        
        paginated = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'assessments': [assessment.to_dict() for assessment in paginated.items],
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

@compliance_bp.route('/compliance/assessments', methods=['POST'])
@jwt_required()
def create_control_assessment():
    """Create a new control assessment."""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Validate required fields
        required_fields = ['control_id', 'status']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': f'{field} is required'
                    }
                }), 400
        
        # Validate status
        valid_statuses = ['compliant', 'non_compliant', 'partially_compliant', 'not_assessed']
        if data['status'] not in valid_statuses:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': f'Status must be one of: {", ".join(valid_statuses)}'
                }
            }), 400
        
        assessment = ControlAssessment(
            control_id=data['control_id'],
            status=data['status'],
            assessor_id=current_user_id,
            evidence=data.get('evidence'),
            remediation_plan=data.get('remediation_plan'),
            next_assessment_date=data.get('next_assessment_date')
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'assessment': assessment.to_dict()
            },
            'message': 'Control assessment created successfully'
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

@compliance_bp.route('/compliance/assessments/<int:assessment_id>', methods=['PUT'])
@jwt_required()
def update_control_assessment(assessment_id):
    """Update a control assessment."""
    try:
        assessment = ControlAssessment.query.get_or_404(assessment_id)
        data = request.get_json()
        
        # Update assessment fields
        updatable_fields = ['status', 'evidence', 'remediation_plan', 'next_assessment_date']
        
        for field in updatable_fields:
            if field in data:
                setattr(assessment, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'assessment': assessment.to_dict()
            },
            'message': 'Control assessment updated successfully'
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

@compliance_bp.route('/compliance/dashboard', methods=['GET'])
@jwt_required()
def get_compliance_dashboard():
    """Get compliance dashboard data."""
    try:
        # Get compliance statistics
        from sqlalchemy import func
        
        total_controls = Control.query.count()
        assessed_controls = ControlAssessment.query.count()
        
        # Get compliance status breakdown
        status_breakdown = db.session.query(
            ControlAssessment.status,
            func.count(ControlAssessment.id).label('count')
        ).group_by(ControlAssessment.status).all()
        
        status_dict = {status: count for status, count in status_breakdown}
        
        # Calculate compliance percentage
        compliant_count = status_dict.get('compliant', 0)
        compliance_percentage = (compliant_count / assessed_controls * 100) if assessed_controls > 0 else 0
        
        # Get framework breakdown
        framework_breakdown = db.session.query(
            ComplianceFramework.name,
            func.count(Control.id).label('total_controls'),
            func.count(ControlAssessment.id).label('assessed_controls')
        ).join(Control).outerjoin(ControlAssessment).group_by(
            ComplianceFramework.name
        ).all()
        
        frameworks = []
        for name, total, assessed in framework_breakdown:
            frameworks.append({
                'name': name,
                'total_controls': total,
                'assessed_controls': assessed,
                'completion_percentage': (assessed / total * 100) if total > 0 else 0
            })
        
        return jsonify({
            'success': True,
            'data': {
                'total_controls': total_controls,
                'assessed_controls': assessed_controls,
                'compliance_percentage': round(compliance_percentage, 1),
                'status_breakdown': status_dict,
                'frameworks': frameworks
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

