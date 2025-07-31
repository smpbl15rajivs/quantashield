from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models import LeakedCredential, ThreatIndicator, ThreatIntelligenceSource, db
from datetime import datetime, timedelta

threat_intelligence_bp = Blueprint('threat_intelligence', __name__)

@threat_intelligence_bp.route('/threat-intelligence/leaked-credentials', methods=['GET'])
@jwt_required()
def get_leaked_credentials():
    """Get leaked credentials with filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        domain = request.args.get('domain')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        query = LeakedCredential.query
        
        if domain:
            query = query.filter(LeakedCredential.domain == domain)
        
        if date_from:
            try:
                date_from_obj = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                query = query.filter(LeakedCredential.discovered_at >= date_from_obj)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid date_from format'
                    }
                }), 400
        
        if date_to:
            try:
                date_to_obj = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                query = query.filter(LeakedCredential.discovered_at <= date_to_obj)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid date_to format'
                    }
                }), 400
        
        # Order by discovery date (newest first)
        query = query.order_by(LeakedCredential.discovered_at.desc())
        
        paginated = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'credentials': [cred.to_dict() for cred in paginated.items],
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

@threat_intelligence_bp.route('/threat-intelligence/indicators', methods=['GET'])
@jwt_required()
def get_threat_indicators():
    """Get threat indicators with filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        indicator_type = request.args.get('type')
        threat_type = request.args.get('threat_type')
        is_active = request.args.get('is_active', type=bool)
        
        query = ThreatIndicator.query
        
        if indicator_type:
            query = query.filter(ThreatIndicator.indicator_type == indicator_type)
        if threat_type:
            query = query.filter(ThreatIndicator.threat_type == threat_type)
        if is_active is not None:
            query = query.filter(ThreatIndicator.is_active == is_active)
        
        # Order by last seen (newest first)
        query = query.order_by(ThreatIndicator.last_seen.desc())
        
        paginated = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'indicators': [indicator.to_dict() for indicator in paginated.items],
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

@threat_intelligence_bp.route('/threat-intelligence/search', methods=['POST'])
@jwt_required()
def search_threat_intelligence():
    """Search across threat intelligence data."""
    try:
        data = request.get_json()
        
        if not data.get('query'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Query is required'
                }
            }), 400
        
        query_term = data['query']
        types = data.get('types', ['email', 'domain', 'ip'])
        date_range = data.get('date_range', {})
        
        results = {
            'credentials': [],
            'indicators': []
        }
        
        # Search leaked credentials
        if 'email' in types or 'domain' in types:
            cred_query = LeakedCredential.query
            
            if 'email' in types:
                cred_query = cred_query.filter(LeakedCredential.email.contains(query_term))
            elif 'domain' in types:
                cred_query = cred_query.filter(LeakedCredential.domain.contains(query_term))
            
            # Apply date range if provided
            if date_range.get('start'):
                start_date = datetime.fromisoformat(date_range['start'])
                cred_query = cred_query.filter(LeakedCredential.discovered_at >= start_date)
            
            if date_range.get('end'):
                end_date = datetime.fromisoformat(date_range['end'])
                cred_query = cred_query.filter(LeakedCredential.discovered_at <= end_date)
            
            credentials = cred_query.limit(50).all()
            results['credentials'] = [cred.to_dict() for cred in credentials]
        
        # Search threat indicators
        indicator_query = ThreatIndicator.query.filter(
            ThreatIndicator.indicator_value.contains(query_term)
        )
        
        if types and set(types).intersection({'ip', 'domain', 'hash'}):
            indicator_query = indicator_query.filter(
                ThreatIndicator.indicator_type.in_(types)
            )
        
        # Apply date range if provided
        if date_range.get('start'):
            start_date = datetime.fromisoformat(date_range['start'])
            indicator_query = indicator_query.filter(ThreatIndicator.first_seen >= start_date)
        
        if date_range.get('end'):
            end_date = datetime.fromisoformat(date_range['end'])
            indicator_query = indicator_query.filter(ThreatIndicator.last_seen <= end_date)
        
        indicators = indicator_query.limit(50).all()
        results['indicators'] = [indicator.to_dict() for indicator in indicators]
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500

@threat_intelligence_bp.route('/threat-intelligence/sources', methods=['GET'])
@jwt_required()
def get_threat_sources():
    """Get all threat intelligence sources."""
    try:
        sources = ThreatIntelligenceSource.query.filter_by(is_active=True).all()
        
        return jsonify({
            'success': True,
            'data': {
                'sources': [source.to_dict() for source in sources]
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

@threat_intelligence_bp.route('/threat-intelligence/stats', methods=['GET'])
@jwt_required()
def get_threat_intelligence_stats():
    """Get threat intelligence statistics."""
    try:
        # Get counts for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        total_credentials = LeakedCredential.query.count()
        recent_credentials = LeakedCredential.query.filter(
            LeakedCredential.discovered_at >= thirty_days_ago
        ).count()
        
        total_indicators = ThreatIndicator.query.count()
        active_indicators = ThreatIndicator.query.filter_by(is_active=True).count()
        
        # Get top domains with leaked credentials
        from sqlalchemy import func
        top_domains = db.session.query(
            LeakedCredential.domain,
            func.count(LeakedCredential.id).label('count')
        ).group_by(LeakedCredential.domain).order_by(
            func.count(LeakedCredential.id).desc()
        ).limit(10).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_credentials': total_credentials,
                'recent_credentials': recent_credentials,
                'total_indicators': total_indicators,
                'active_indicators': active_indicators,
                'top_domains': [{'domain': domain, 'count': count} for domain, count in top_domains]
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

