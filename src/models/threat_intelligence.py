from datetime import datetime
from .user import db

class ThreatIntelligenceSource(db.Model):
    __tablename__ = 'threat_intelligence_sources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # telegram, forum, marketplace
    url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    last_collected = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    leaked_credentials = db.relationship('LeakedCredential', back_populates='source', cascade='all, delete-orphan')
    threat_indicators = db.relationship('ThreatIndicator', back_populates='source', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ThreatIntelligenceSource {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'url': self.url,
            'is_active': self.is_active,
            'last_collected': self.last_collected.isoformat() if self.last_collected else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LeakedCredential(db.Model):
    __tablename__ = 'leaked_credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    domain = db.Column(db.String(100))
    password_hash = db.Column(db.String(255))
    source_id = db.Column(db.Integer, db.ForeignKey('threat_intelligence_sources.id'))
    discovered_at = db.Column(db.DateTime, default=datetime.utcnow)
    malware_family = db.Column(db.String(50))  # redline, raccoon, meta_stealer, etc.
    additional_data = db.Column(db.JSON)  # Store any additional extracted data
    
    # Relationships
    source = db.relationship('ThreatIntelligenceSource', back_populates='leaked_credentials')

    def __repr__(self):
        return f'<LeakedCredential {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'domain': self.domain,
            'source_id': self.source_id,
            'discovered_at': self.discovered_at.isoformat() if self.discovered_at else None,
            'malware_family': self.malware_family,
            'additional_data': self.additional_data,
            'source': self.source.name if self.source else None
        }

class ThreatIndicator(db.Model):
    __tablename__ = 'threat_indicators'
    
    id = db.Column(db.Integer, primary_key=True)
    indicator_type = db.Column(db.String(50))  # ip, domain, hash, email
    indicator_value = db.Column(db.String(500), nullable=False)
    threat_type = db.Column(db.String(50))  # malware, phishing, c2, etc.
    confidence_score = db.Column(db.Integer)  # 0-100
    source_id = db.Column(db.Integer, db.ForeignKey('threat_intelligence_sources.id'))
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    source = db.relationship('ThreatIntelligenceSource', back_populates='threat_indicators')

    def __repr__(self):
        return f'<ThreatIndicator {self.indicator_type}:{self.indicator_value}>'

    def to_dict(self):
        return {
            'id': self.id,
            'indicator_type': self.indicator_type,
            'indicator_value': self.indicator_value,
            'threat_type': self.threat_type,
            'confidence_score': self.confidence_score,
            'source_id': self.source_id,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'is_active': self.is_active,
            'source': self.source.name if self.source else None
        }

