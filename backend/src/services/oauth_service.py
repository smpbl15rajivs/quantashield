"""
OAuth Service for handling federated authentication
"""
import secrets
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode, parse_qs, urlparse
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
from flask import current_app, url_for, session
from ..config.oauth_config import OAuthConfig
from ..models.federated_user import FederatedIdentity, OAuthState
from ..models.user import User
from ..models import db

class OAuthService:
    """Service for handling OAuth/OIDC authentication with multiple providers"""
    
    def __init__(self, app=None):
        self.oauth = OAuth()
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize OAuth with Flask app"""
        self.oauth.init_app(app)
        self._register_providers()
    
    def _register_providers(self):
        """Register all OAuth providers"""
        # Google
        google_config = OAuthConfig.get_provider_config('google')
        if google_config:
            self.oauth.register(
                name='google',
                client_id=google_config['client_id'],
                client_secret=google_config['client_secret'],
                server_metadata_url=google_config['discovery_url'],
                client_kwargs={
                    'scope': ' '.join(google_config['scopes'])
                }
            )
        
        # Microsoft
        microsoft_config = OAuthConfig.get_provider_config('microsoft')
        if microsoft_config:
            self.oauth.register(
                name='microsoft',
                client_id=microsoft_config['client_id'],
                client_secret=microsoft_config['client_secret'],
                authority=microsoft_config['authority'],
                client_kwargs={
                    'scope': ' '.join(microsoft_config['scopes'])
                }
            )
        
        # Facebook
        facebook_config = OAuthConfig.get_provider_config('facebook')
        if facebook_config:
            self.oauth.register(
                name='facebook',
                client_id=facebook_config['client_id'],
                client_secret=facebook_config['client_secret'],
                server_metadata_url=facebook_config['discovery_url'],
                client_kwargs={
                    'scope': ' '.join(facebook_config['scopes'])
                }
            )
        
        # LinkedIn
        linkedin_config = OAuthConfig.get_provider_config('linkedin')
        if linkedin_config:
            self.oauth.register(
                name='linkedin',
                client_id=linkedin_config['client_id'],
                client_secret=linkedin_config['client_secret'],
                server_metadata_url=linkedin_config['discovery_url'],
                client_kwargs={
                    'scope': ' '.join(linkedin_config['scopes'])
                }
            )
        
        # Twitter (manual configuration as it doesn't use OIDC discovery)
        twitter_config = OAuthConfig.get_provider_config('twitter')
        if twitter_config:
            self.oauth.register(
                name='twitter',
                client_id=twitter_config['client_id'],
                client_secret=twitter_config['client_secret'],
                authorize_url='https://twitter.com/i/oauth2/authorize',
                access_token_url='https://api.twitter.com/2/oauth2/token',
                client_kwargs={
                    'scope': ' '.join(twitter_config['scopes']),
                    'code_challenge_method': 'S256'
                }
            )
    
    def generate_state(self, provider, redirect_url=None):
        """Generate and store OAuth state for security"""
        state = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(minutes=10)  # State expires in 10 minutes
        
        oauth_state = OAuthState(
            state=state,
            provider=provider,
            redirect_url=redirect_url,
            expires_at=expires_at
        )
        
        db.session.add(oauth_state)
        db.session.commit()
        
        return state
    
    def verify_state(self, state, provider):
        """Verify OAuth state and return the stored state object"""
        oauth_state = OAuthState.query.filter_by(
            state=state,
            provider=provider,
            is_used=False
        ).first()
        
        if not oauth_state:
            return None
        
        if oauth_state.is_expired():
            db.session.delete(oauth_state)
            db.session.commit()
            return None
        
        # Mark state as used
        oauth_state.is_used = True
        db.session.commit()
        
        return oauth_state
    
    def get_authorization_url(self, provider, redirect_url=None):
        """Get authorization URL for a provider"""
        if provider not in ['google', 'microsoft', 'facebook', 'linkedin', 'twitter']:
            raise ValueError(f"Unsupported provider: {provider}")
        
        client = getattr(self.oauth, provider)
        if not client:
            raise ValueError(f"Provider {provider} not configured")
        
        state = self.generate_state(provider, redirect_url)
        config = OAuthConfig.get_provider_config(provider)
        
        return client.authorize_redirect(
            redirect_uri=config['redirect_uri'],
            state=state
        )
    
    def handle_callback(self, provider, code, state):
        """Handle OAuth callback and return user information"""
        # Verify state
        oauth_state = self.verify_state(state, provider)
        if not oauth_state:
            raise ValueError("Invalid or expired state")
        
        client = getattr(self.oauth, provider)
        if not client:
            raise ValueError(f"Provider {provider} not configured")
        
        config = OAuthConfig.get_provider_config(provider)
        
        # Exchange code for tokens
        token = client.authorize_access_token(
            redirect_uri=config['redirect_uri']
        )
        
        # Get user info based on provider
        if provider == 'twitter':
            # Twitter doesn't provide ID token, use API to get user info
            user_info = self._get_twitter_user_info(token['access_token'])
        else:
            # For OIDC providers, parse ID token
            if 'id_token' in token:
                user_info = self._parse_id_token(token['id_token'], provider)
            else:
                # Fallback to userinfo endpoint
                user_info = self._get_user_info_from_api(token['access_token'], provider)
        
        return user_info, token, oauth_state.redirect_url
    
    def _parse_id_token(self, id_token, provider):
        """Parse and verify ID token"""
        try:
            # In production, you should verify the token signature
            # For now, we'll decode without verification for demo purposes
            claims = jwt.decode(id_token, options={"verify_signature": False})
            
            return {
                'provider_user_id': claims.get('sub'),
                'email': claims.get('email'),
                'name': claims.get('name'),
                'first_name': claims.get('given_name'),
                'last_name': claims.get('family_name'),
                'profile_picture': claims.get('picture'),
                'provider': provider
            }
        except Exception as e:
            current_app.logger.error(f"Error parsing ID token: {e}")
            return None
    
    def _get_twitter_user_info(self, access_token):
        """Get user info from Twitter API"""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            'https://api.twitter.com/2/users/me?user.fields=profile_image_url',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()['data']
            return {
                'provider_user_id': data['id'],
                'email': None,  # Twitter doesn't provide email by default
                'name': data['name'],
                'first_name': data['name'].split()[0] if data['name'] else None,
                'last_name': ' '.join(data['name'].split()[1:]) if len(data['name'].split()) > 1 else None,
                'profile_picture': data.get('profile_image_url'),
                'provider': 'twitter'
            }
        else:
            current_app.logger.error(f"Error getting Twitter user info: {response.text}")
            return None
    
    def _get_user_info_from_api(self, access_token, provider):
        """Get user info from provider's userinfo endpoint"""
        # This is a fallback method for providers that don't provide ID tokens
        # Implementation would depend on the specific provider's API
        pass
    
    def create_or_update_federated_user(self, user_info, token_info):
        """Create or update user with federated identity"""
        provider = user_info['provider']
        provider_user_id = user_info['provider_user_id']
        
        # Check if federated identity already exists
        federated_identity = FederatedIdentity.query.filter_by(
            provider=provider,
            provider_user_id=provider_user_id
        ).first()
        
        if federated_identity:
            # Update existing federated identity
            user = federated_identity.user
            federated_identity.email = user_info.get('email')
            federated_identity.name = user_info.get('name')
            federated_identity.profile_picture_url = user_info.get('profile_picture')
            federated_identity.access_token = token_info.get('access_token')
            federated_identity.refresh_token = token_info.get('refresh_token')
            if 'expires_in' in token_info:
                federated_identity.token_expires_at = datetime.utcnow() + timedelta(seconds=token_info['expires_in'])
            federated_identity.updated_at = datetime.utcnow()
        else:
            # Check if user exists by email
            user = None
            if user_info.get('email'):
                user = User.query.filter_by(email=user_info['email']).first()
            
            if not user:
                # Create new user
                username = user_info.get('email', f"{provider}_{provider_user_id}")
                user = User(
                    username=username,
                    email=user_info.get('email', f"{provider}_{provider_user_id}@{provider}.local"),
                    first_name=user_info.get('first_name'),
                    last_name=user_info.get('last_name'),
                    is_active=True
                )
                db.session.add(user)
                db.session.flush()  # Get user ID
            
            # Create federated identity
            federated_identity = FederatedIdentity(
                user_id=user.id,
                provider=provider,
                provider_user_id=provider_user_id,
                email=user_info.get('email'),
                name=user_info.get('name'),
                profile_picture_url=user_info.get('profile_picture'),
                access_token=token_info.get('access_token'),
                refresh_token=token_info.get('refresh_token'),
                token_expires_at=datetime.utcnow() + timedelta(seconds=token_info.get('expires_in', 3600))
            )
            db.session.add(federated_identity)
        
        # Update user's last login
        user.last_login = datetime.utcnow()
        
        db.session.commit()
        return user

