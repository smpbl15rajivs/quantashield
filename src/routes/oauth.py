"""
OAuth routes for federated authentication
"""
from flask import Blueprint, request, jsonify, redirect, url_for, session, current_app
from ..services.oauth_service import OAuthService
from ..models.user import User
from ..models import db
import jwt
from datetime import datetime, timedelta

oauth_bp = Blueprint('oauth', __name__, url_prefix='/api/auth')

# Initialize OAuth service
oauth_service = OAuthService()

@oauth_bp.route('/providers', methods=['GET'])
def get_providers():
    """Get list of available OAuth providers"""
    providers = [
        {
            'name': 'google',
            'display_name': 'Google',
            'icon': 'google',
            'color': '#4285f4'
        },
        {
            'name': 'microsoft',
            'display_name': 'Microsoft',
            'icon': 'microsoft',
            'color': '#00a1f1'
        },
        {
            'name': 'facebook',
            'display_name': 'Facebook',
            'icon': 'facebook',
            'color': '#1877f2'
        },
        {
            'name': 'linkedin',
            'display_name': 'LinkedIn',
            'icon': 'linkedin',
            'color': '#0077b5'
        },
        {
            'name': 'twitter',
            'display_name': 'Twitter',
            'icon': 'twitter',
            'color': '#1da1f2'
        }
    ]
    
    return jsonify({
        'success': True,
        'providers': providers
    })

@oauth_bp.route('/<provider>/login', methods=['GET'])
def oauth_login(provider):
    """Initiate OAuth login for a provider"""
    try:
        redirect_url = request.args.get('redirect_url')
        authorization_url = oauth_service.get_authorization_url(provider, redirect_url)
        return authorization_url
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f"OAuth login error for {provider}: {e}")
        return jsonify({
            'success': False,
            'error': 'Authentication service temporarily unavailable'
        }), 500

@oauth_bp.route('/<provider>/callback', methods=['GET'])
def oauth_callback(provider):
    """Handle OAuth callback from provider"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            return jsonify({
                'success': False,
                'error': f'OAuth error: {error}'
            }), 400
        
        if not code or not state:
            return jsonify({
                'success': False,
                'error': 'Missing authorization code or state'
            }), 400
        
        # Handle the callback
        user_info, token_info, redirect_url = oauth_service.handle_callback(provider, code, state)
        
        if not user_info:
            return jsonify({
                'success': False,
                'error': 'Failed to get user information'
            }), 400
        
        # Create or update user
        user = oauth_service.create_or_update_federated_user(user_info, token_info)
        
        # Generate JWT token for the user
        token = generate_jwt_token(user)
        
        # If there's a redirect URL, redirect to frontend with token
        if redirect_url:
            return redirect(f"{redirect_url}?token={token}")
        
        # Otherwise, return JSON response
        return jsonify({
            'success': True,
            'message': f'Successfully authenticated with {provider}',
            'user': user.to_dict(),
            'token': token
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f"OAuth callback error for {provider}: {e}")
        return jsonify({
            'success': False,
            'error': 'Authentication failed'
        }), 500

@oauth_bp.route('/link/<provider>', methods=['POST'])
def link_provider(provider):
    """Link a provider to an existing user account"""
    try:
        # This endpoint would be used when a logged-in user wants to link
        # an additional provider to their account
        
        # Get current user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.query.get(user_id)
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
        # Check if user already has this provider linked
        if user.has_federated_identity(provider):
            return jsonify({
                'success': False,
                'error': f'{provider.title()} account is already linked'
            }), 400
        
        # Generate authorization URL for linking
        authorization_url = oauth_service.get_authorization_url(
            provider, 
            redirect_url=f"{request.host_url}api/auth/{provider}/link-callback"
        )
        
        return authorization_url
        
    except Exception as e:
        current_app.logger.error(f"Provider linking error for {provider}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to initiate provider linking'
        }), 500

@oauth_bp.route('/<provider>/unlink', methods=['DELETE'])
def unlink_provider(provider):
    """Unlink a provider from user account"""
    try:
        # Get current user from JWT token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.query.get(user_id)
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
        # Check if user has this provider linked
        federated_identity = user.get_federated_identity(provider)
        if not federated_identity:
            return jsonify({
                'success': False,
                'error': f'{provider.title()} account is not linked'
            }), 400
        
        # Don't allow unlinking if it's the only authentication method
        if not user.password_hash and len([fi for fi in user.federated_identities if fi.is_active]) == 1:
            return jsonify({
                'success': False,
                'error': 'Cannot unlink the only authentication method. Please set a password first.'
            }), 400
        
        # Deactivate the federated identity
        federated_identity.is_active = False
        federated_identity.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{provider.title()} account unlinked successfully'
        })
        
    except Exception as e:
        current_app.logger.error(f"Provider unlinking error for {provider}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to unlink provider'
        }), 500

def generate_jwt_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def init_oauth_service(app):
    """Initialize OAuth service with Flask app"""
    oauth_service.init_app(app)

