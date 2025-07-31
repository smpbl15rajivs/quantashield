from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import Asset, Incident, User, LeakedCredential, ThreatIndicator, db
from datetime import datetime, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    """Get comprehensive dashboard data."""
    try:
        # Get basic counts
        total_assets = Asset.query.count()
        total_users = User.query.count()
        
        # Get incident statistics
        open_incidents = Incident.query.filter(
            Incident.status.in_(['open', 'investigating'])
        ).count()
        
        critical_incidents = Incident.query.filter_by(severity='critical').count()
        
        # Get recent incidents (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_incidents_query = Incident.query.filter(
            Incident.created_at >= seven_days_ago
        ).order_by(Incident.created_at.desc()).limit(5)
        
        recent_incidents = [incident.to_dict() for incident in recent_incidents_query]
        
        # Get vulnerability statistics
        from src.models import AssetVulnerability
        critical_vulnerabilities = AssetVulnerability.query.join(
            Asset
        ).filter(AssetVulnerability.status == 'open').count()
        
        # Get threat intelligence statistics
        recent_credentials = LeakedCredential.query.filter(
            LeakedCredential.discovered_at >= seven_days_ago
        ).count()
        
        active_threats = ThreatIndicator.query.filter_by(is_active=True).count()
        
        # Get security scorecard
        latest_scorecard = SecurityScorecard.query.order_by(
            SecurityScorecard.calculated_at.desc()
        ).first()
        
        security_score = latest_scorecard.overall_score if latest_scorecard else 0
        
        # Get asset breakdown by type
        asset_breakdown = db.session.query(
            Asset.type,
            func.count(Asset.id).label('count')
        ).group_by(Asset.type).all()
        
        asset_types = {asset_type: count for asset_type, count in asset_breakdown}
        
        # Get incident trends (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        incident_trends = []
        
        for i in range(30):
            date = thirty_days_ago + timedelta(days=i)
            day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            daily_incidents = Incident.query.filter(
                Incident.created_at >= day_start,
                Incident.created_at < day_end
            ).count()
            
            incident_trends.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'count': daily_incidents
            })
        
        # Get top threat indicators
        top_threats = ThreatIndicator.query.filter_by(
            is_active=True
        ).order_by(ThreatIndicator.confidence_score.desc()).limit(5).all()
        
        return jsonify({
            'success': True,
            'data': {
                'summary': {
                    'total_assets': total_assets,
                    'total_users': total_users,
                    'open_incidents': open_incidents,
                    'critical_incidents': critical_incidents,
                    'critical_vulnerabilities': critical_vulnerabilities,
                    'security_score': security_score,
                    'recent_credentials': recent_credentials,
                    'active_threats': active_threats
                },
                'recent_incidents': recent_incidents,
                'asset_breakdown': asset_types,
                'incident_trends': incident_trends,
                'top_threats': [threat.to_dict() for threat in top_threats],
                'scorecard_factors': latest_scorecard.factors if latest_scorecard else {}
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

@dashboard_bp.route('/dashboard/widgets/<widget_type>', methods=['GET'])
@jwt_required()
def get_widget_data(widget_type):
    """Get data for a specific dashboard widget."""
    try:
        if widget_type == 'security_metrics':
            # Get key security metrics
            total_assets = Asset.query.count()
            active_assets = Asset.query.filter_by(status='active').count()
            
            # Get vulnerability metrics
            from src.models import AssetVulnerability, Vulnerability
            total_vulnerabilities = AssetVulnerability.query.count()
            critical_vulns = AssetVulnerability.query.join(Vulnerability).filter(
                Vulnerability.severity == 'critical',
                AssetVulnerability.status == 'open'
            ).count()
            
            return jsonify({
                'success': True,
                'data': {
                    'total_assets': total_assets,
                    'active_assets': active_assets,
                    'total_vulnerabilities': total_vulnerabilities,
                    'critical_vulnerabilities': critical_vulns
                }
            })
            
        elif widget_type == 'threat_landscape':
            # Get threat landscape data
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            new_threats = ThreatIndicator.query.filter(
                ThreatIndicator.first_seen >= thirty_days_ago
            ).count()
            
            new_credentials = LeakedCredential.query.filter(
                LeakedCredential.discovered_at >= thirty_days_ago
            ).count()
            
            # Get threat types breakdown
            threat_types = db.session.query(
                ThreatIndicator.threat_type,
                func.count(ThreatIndicator.id).label('count')
            ).filter_by(is_active=True).group_by(
                ThreatIndicator.threat_type
            ).all()
            
            return jsonify({
                'success': True,
                'data': {
                    'new_threats': new_threats,
                    'new_credentials': new_credentials,
                    'threat_types': {threat_type: count for threat_type, count in threat_types}
                }
            })
            
        elif widget_type == 'compliance_status':
            # Get compliance status
            from src.models import ControlAssessment
            
            total_assessments = ControlAssessment.query.count()
            compliant_assessments = ControlAssessment.query.filter_by(
                status='compliant'
            ).count()
            
            compliance_rate = (compliant_assessments / total_assessments * 100) if total_assessments > 0 else 0
            
            return jsonify({
                'success': True,
                'data': {
                    'total_assessments': total_assessments,
                    'compliant_assessments': compliant_assessments,
                    'compliance_rate': round(compliance_rate, 1)
                }
            })
            
        else:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_WIDGET_TYPE',
                    'message': f'Unknown widget type: {widget_type}'
                }
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500

@dashboard_bp.route('/dashboard/alerts', methods=['GET'])
@jwt_required()
def get_dashboard_alerts():
    """Get dashboard alerts and notifications."""
    try:
        alerts = []
        
        # Check for critical incidents
        critical_incidents = Incident.query.filter_by(
            severity='critical',
            status='open'
        ).count()
        
        if critical_incidents > 0:
            alerts.append({
                'type': 'critical',
                'title': 'Critical Incidents',
                'message': f'{critical_incidents} critical incident(s) require immediate attention',
                'count': critical_incidents
            })
        
        # Check for recent credential leaks
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        recent_leaks = LeakedCredential.query.filter(
            LeakedCredential.discovered_at >= twenty_four_hours_ago
        ).count()
        
        if recent_leaks > 0:
            alerts.append({
                'type': 'warning',
                'title': 'New Credential Leaks',
                'message': f'{recent_leaks} new credential leak(s) detected in the last 24 hours',
                'count': recent_leaks
            })
        
        # Check for overdue assessments
        from src.models import ControlAssessment
        overdue_assessments = ControlAssessment.query.filter(
            ControlAssessment.next_assessment_date < datetime.utcnow().date()
        ).count()
        
        if overdue_assessments > 0:
            alerts.append({
                'type': 'info',
                'title': 'Overdue Assessments',
                'message': f'{overdue_assessments} compliance assessment(s) are overdue',
                'count': overdue_assessments
            })
        
        return jsonify({
            'success': True,
            'data': {
                'alerts': alerts
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

