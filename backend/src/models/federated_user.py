"""
Database models for federated identity management
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class FederatedIdentity(db.Model):
    """Model for storing federated identity information"""
    __tablename__ = 'federated_identities'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    provider = Column(String(50), nullable=False)  # google, microsoft, facebook, linkedin, twitter
    provider_user_id = Column(String(255), nullable=False)  # Unique ID from the provider
    email = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    profile_picture_url = Column(Text, nullable=True)
    access_token = Column(Text, nullable=True)  # Encrypted in production
    refresh_token = Column(Text, nullable=True)  # Encrypted in production
    token_expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to User model
    user = relationship("User", back_populates="federated_identities")
    
    # Unique constraint to prevent duplicate provider accounts for same user
    __table_args__ = (
        db.UniqueConstraint('provider', 'provider_user_id', name='unique_provider_user'),
    )
    
    def __repr__(self):
        return f'<FederatedIdentity {self.provider}:{self.provider_user_id}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'provider': self.provider,
            'provider_user_id': self.provider_user_id,
            'email': self.email,
            'name': self.name,
            'profile_picture_url': self.profile_picture_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class OAuthState(db.Model):
    """Model for storing OAuth state parameters for security"""
    __tablename__ = 'oauth_states'
    
    id = Column(Integer, primary_key=True)
    state = Column(String(255), unique=True, nullable=False)
    provider = Column(String(50), nullable=False)
    redirect_url = Column(Text, nullable=True)  # Where to redirect after successful auth
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    
    def __repr__(self):
        return f'<OAuthState {self.state}>'
    
    def is_expired(self):
        """Check if the state has expired"""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'state': self.state,
            'provider': self.provider,
            'redirect_url': self.redirect_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_used': self.is_used
        }

