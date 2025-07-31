from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.real_time_monitoring import monitoring_service
from datetime import datetime

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/api/monitoring/status', methods=['GET'])
@jwt_required()
def get_monitoring_status():
    """Get real-time monitoring status"""
    try:
        status = monitoring_service.get_monitoring_status()
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@monitoring_bp.route('/api/monitoring/start', methods=['POST'])
@jwt_required()
def start_monitoring():
    """Start real-time monitoring"""
    try:
        monitoring_service.start_monitoring()
        return jsonify({
            'success': True,
            'message': 'Real-time monitoring started'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@monitoring_bp.route('/api/monitoring/stop', methods=['POST'])
@jwt_required()
def stop_monitoring():
    """Stop real-time monitoring"""
    try:
        monitoring_service.stop_monitoring()
        return jsonify({
            'success': True,
            'message': 'Real-time monitoring stopped'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@monitoring_bp.route('/api/monitoring/events', methods=['GET'])
@jwt_required()
def get_recent_events():
    """Get recent security events"""
    try:
        limit = int(request.args.get('limit', 50))
        events = monitoring_service.get_recent_events(limit=limit)
        
        return jsonify({
            'success': True,
            'data': events,
            'count': len(events)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@monitoring_bp.route('/api/monitoring/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    """Get security alerts"""
    try:
        unresolved_only = request.args.get('unresolved_only', 'false').lower() == 'true'
        alerts = monitoring_service.get_alerts(unresolved_only=unresolved_only)
        
        return jsonify({
            'success': True,
            'data': alerts,
            'count': len(alerts)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@monitoring_bp.route('/api/monitoring/alerts/<alert_id>/acknowledge', methods=['POST'])
@jwt_required()
def acknowledge_alert(alert_id):
    """Acknowledge a security alert"""
    try:
        success = monitoring_service.acknowledge_alert(alert_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Alert acknowledged'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Alert not found'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@monitoring_bp.route('/api/monitoring/alerts/<alert_id>/resolve', methods=['POST'])
@jwt_required()
def resolve_alert(alert_id):
    """Resolve a security alert"""
    try:
        success = monitoring_service.resolve_alert(alert_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Alert resolved'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Alert not found'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@monitoring_bp.route('/api/monitoring/subscribe', methods=['POST'])
@jwt_required()
def subscribe_to_events():
    """Subscribe to real-time events (WebSocket alternative)"""
    try:
        user_id = get_jwt_identity()
        
        # For demo purposes, just register the subscription
        # In a real implementation, this would set up WebSocket or SSE
        def event_callback(event):
            # This would normally send the event via WebSocket
            pass
        
        monitoring_service.subscribe(f"user_{user_id}", event_callback)
        
        return jsonify({
            'success': True,
            'message': 'Subscribed to real-time events'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@monitoring_bp.route('/api/monitoring/unsubscribe', methods=['POST'])
@jwt_required()
def unsubscribe_from_events():
    """Unsubscribe from real-time events"""
    try:
        user_id = get_jwt_identity()
        monitoring_service.unsubscribe(f"user_{user_id}")
        
        return jsonify({
            'success': True,
            'message': 'Unsubscribed from real-time events'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

