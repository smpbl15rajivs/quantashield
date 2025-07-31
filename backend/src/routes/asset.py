from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import Asset, db, Vulnerability

asset_bp = Blueprint('asset', __name__)

@asset_bp.route('/assets', methods=['GET'])
@jwt_required()
def get_assets():
    """Get all assets with filtering and pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        asset_type = request.args.get('type')
        status = request.args.get('status')
        category = request.args.get('category')
        
        query = Asset.query
        
        if asset_type:
            query = query.filter(Asset.type == asset_type)
        if status:
            query = query.filter(Asset.status == status)
        if category:
            query = query.filter(Asset.category == category)
        
        paginated = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'assets': [asset.to_dict() for asset in paginated.items],
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

@asset_bp.route('/assets', methods=['POST'])
@jwt_required()
def create_asset():
    """Create a new asset."""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Validate required fields
        required_fields = ['name', 'type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': f'{field} is required'
                    }
                }), 400
        
        asset = Asset(
            name=data['name'],
            type=data['type'],
            category=data.get('category'),
            ip_address=data.get('ip_address'),
            mac_address=data.get('mac_address'),
            operating_system=data.get('operating_system'),
            version=data.get('version'),
            owner_id=data.get('owner_id', current_user_id),
            location=data.get('location'),
            status=data.get('status', 'active')
        )
        
        db.session.add(asset)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'asset': asset.to_dict()
            },
            'message': 'Asset created successfully'
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

@asset_bp.route('/assets/<int:asset_id>', methods=['GET'])
@jwt_required()
def get_asset(asset_id):
    """Get a specific asset by ID."""
    try:
        asset = Asset.query.get_or_404(asset_id)
        return jsonify({
            'success': True,
            'data': {
                'asset': asset.to_dict()
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

@asset_bp.route('/assets/<int:asset_id>', methods=['PUT'])
@jwt_required()
def update_asset(asset_id):
    """Update an asset."""
    try:
        asset = Asset.query.get_or_404(asset_id)
        data = request.get_json()
        
        # Update asset fields
        updatable_fields = [
            'name', 'type', 'category', 'ip_address', 'mac_address',
            'operating_system', 'version', 'owner_id', 'location', 'status'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(asset, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'asset': asset.to_dict()
            },
            'message': 'Asset updated successfully'
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

@asset_bp.route('/assets/<int:asset_id>', methods=['DELETE'])
@jwt_required()
def delete_asset(asset_id):
    """Delete an asset."""
    try:
        asset = Asset.query.get_or_404(asset_id)
        db.session.delete(asset)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Asset deleted successfully'
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

@asset_bp.route('/assets/<int:asset_id>/vulnerabilities', methods=['GET'])
@jwt_required()
def get_asset_vulnerabilities(asset_id):
    """Get vulnerabilities for a specific asset."""
    try:
        asset = Asset.query.get_or_404(asset_id)
        vulnerabilities = [av.to_dict() for av in asset.vulnerabilities]
        
        return jsonify({
            'success': True,
            'data': {
                'asset_id': asset_id,
                'vulnerabilities': vulnerabilities
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

