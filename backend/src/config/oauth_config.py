"""
OAuth Configuration for Federated Identity Providers
"""
import os

class OAuthConfig:
    """OAuth configuration for all supported Identity Providers"""
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your-google-client-id')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid_connect_configuration"
    
    # Microsoft OAuth Configuration
    MICROSOFT_CLIENT_ID = os.environ.get('MICROSOFT_CLIENT_ID', 'your-microsoft-client-id')
    MICROSOFT_CLIENT_SECRET = os.environ.get('MICROSOFT_CLIENT_SECRET', 'your-microsoft-client-secret')
    MICROSOFT_TENANT_ID = os.environ.get('MICROSOFT_TENANT_ID', 'common')  # 'common' for multi-tenant
    MICROSOFT_AUTHORITY = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}"
    
    # Facebook OAuth Configuration
    FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID', 'your-facebook-client-id')
    FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET', 'your-facebook-client-secret')
    FACEBOOK_DISCOVERY_URL = "https://www.facebook.com/.well-known/openid_connect/"
    
    # LinkedIn OAuth Configuration
    LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID', 'your-linkedin-client-id')
    LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET', 'your-linkedin-client-secret')
    LINKEDIN_DISCOVERY_URL = "https://www.linkedin.com/oauth/.well-known/openid_connect_configuration"
    
    # Twitter OAuth Configuration
    TWITTER_CLIENT_ID = os.environ.get('TWITTER_CLIENT_ID', 'your-twitter-client-id')
    TWITTER_CLIENT_SECRET = os.environ.get('TWITTER_CLIENT_SECRET', 'your-twitter-client-secret')
    
    # Common OAuth Settings
    OAUTH_REDIRECT_URI_BASE = os.environ.get('OAUTH_REDIRECT_URI_BASE', 'http://localhost:5000')
    
    @classmethod
    def get_redirect_uri(cls, provider):
        """Get the redirect URI for a specific provider"""
        return f"{cls.OAUTH_REDIRECT_URI_BASE}/api/auth/{provider}/callback"
    
    @classmethod
    def get_provider_config(cls, provider):
        """Get configuration for a specific provider"""
        configs = {
            'google': {
                'client_id': cls.GOOGLE_CLIENT_ID,
                'client_secret': cls.GOOGLE_CLIENT_SECRET,
                'discovery_url': cls.GOOGLE_DISCOVERY_URL,
                'scopes': ['openid', 'email', 'profile'],
                'redirect_uri': cls.get_redirect_uri('google')
            },
            'microsoft': {
                'client_id': cls.MICROSOFT_CLIENT_ID,
                'client_secret': cls.MICROSOFT_CLIENT_SECRET,
                'authority': cls.MICROSOFT_AUTHORITY,
                'scopes': ['openid', 'email', 'profile'],
                'redirect_uri': cls.get_redirect_uri('microsoft')
            },
            'facebook': {
                'client_id': cls.FACEBOOK_CLIENT_ID,
                'client_secret': cls.FACEBOOK_CLIENT_SECRET,
                'discovery_url': cls.FACEBOOK_DISCOVERY_URL,
                'scopes': ['openid', 'email', 'public_profile'],
                'redirect_uri': cls.get_redirect_uri('facebook')
            },
            'linkedin': {
                'client_id': cls.LINKEDIN_CLIENT_ID,
                'client_secret': cls.LINKEDIN_CLIENT_SECRET,
                'discovery_url': cls.LINKEDIN_DISCOVERY_URL,
                'scopes': ['openid', 'email', 'profile'],
                'redirect_uri': cls.get_redirect_uri('linkedin')
            },
            'twitter': {
                'client_id': cls.TWITTER_CLIENT_ID,
                'client_secret': cls.TWITTER_CLIENT_SECRET,
                'scopes': ['users.read', 'offline.access'],
                'redirect_uri': cls.get_redirect_uri('twitter')
            }
        }
        return configs.get(provider)

