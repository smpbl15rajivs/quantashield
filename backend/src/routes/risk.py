from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import RiskAssessment, db

risk_bp = Blueprint('risk', __name__)

@risk_bp.route('/risk/scorecard', methods=['GET'])
@jwt_required()
def get_security_scorecard():
    """Get the latest security scorecard."""
    try:
        # Get the most recent scorecard
        scorecard = SecurityScorecard.query.order_by(SecurityScorecard.calculated_at.desc()).first()
        
        if not scorecard:
            # Generate a sample scorecard if none exists
            sample_factors = {
                'asset_management': 85,
                'vulnerability_management': 78,
                'incident_response': 82,
                'compliance': 90,
                'user_management': 75,
                'threat_intelligence': 88
            }
            
            overall_score = sum(sample_factors.values()) // len(sample_factors)
            
            scorecard = SecurityScorecard(
                organization_unit='Default',
                overall_score=overall_score,
                factors=sample_factors
            )
            db.session.add(scorecard)
            db.session.commit()
        
        # Generate recommendations based on scores
        recommendations = []
        if scorecard.factors:
            for factor, score in scorecard.factors.items():
                if score < 80:
                    recommendations.append(f"Improve {factor.replace('_', ' ').title()}")
        
        return jsonify({
            'success': True,
            'data': {
                'overall_score': scorecard.overall_score,
                'calculated_at': scorecard.calculated_at.isoformat(),
                'factors': scorecard.factors,
                'trend': 'stable',  # This would be calculated based on historical data
                'recommendations': recommendations
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

@risk_bp.route('/risk/assessments', methods=['GET'])
@jwt_required()
def get_risk_assessments():
    """Get all risk assessments with filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        asset_id = request.args.get('asset_id', type=int)
        risk_factor_id = request.args.get('risk_factor_id', type=int)
        
        query = RiskAssessment.query
        
        if asset_id:
            query = query.filter(RiskAssessment.asset_id == asset_id)
        if risk_factor_id:
            query = query.filter(RiskAssessment.risk_factor_id == risk_factor_id)
        
        # Order by assessment date (newest first)
        query = query.order_by(RiskAssessment.assessment_date.desc())
        
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

@risk_bp.route('/risk/assessments', methods=['POST'])
@jwt_required()
def create_risk_assessment():
    """Create a new risk assessment."""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Validate required fields
        required_fields = ['asset_id', 'risk_factor_id', 'score']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': f'{field} is required'
                    }
                }), 400
        
        # Validate score range
        if not (0 <= data['score'] <= 100):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Score must be between 0 and 100'
                }
            }), 400
        
        assessment = RiskAssessment(
            asset_id=data['asset_id'],
            risk_factor_id=data['risk_factor_id'],
            score=data['score'],
            assessor_id=current_user_id,
            notes=data.get('notes')
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'assessment': assessment.to_dict()
            },
            'message': 'Risk assessment created successfully'
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

@risk_bp.route('/risk/factors', methods=['GET'])
@jwt_required()
def get_risk_factors():
    """Get all risk factors."""
    try:
        factors = RiskFactor.query.filter_by(is_active=True).all()
        
        return jsonify({
            'success': True,
            'data': {
                'risk_factors': [factor.to_dict() for factor in factors]
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

@risk_bp.route('/risk/factors', methods=['POST'])
@jwt_required()
def create_risk_factor():
    """Create a new risk factor."""
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
        
        risk_factor = RiskFactor(
            name=data['name'],
            category=data.get('category'),
            weight=data.get('weight', 1.0),
            description=data.get('description')
        )
        
        db.session.add(risk_factor)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'risk_factor': risk_factor.to_dict()
            },
            'message': 'Risk factor created successfully'
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

