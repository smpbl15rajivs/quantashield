from datetime import datetime
from .user import db

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # server, workstation, network_device, software, etc.
    category = db.Column(db.String(50))  # critical, high, medium, low
    ip_address = db.Column(db.String(45))  # Supports IPv4 and IPv6
    mac_address = db.Column(db.String(17))
    operating_system = db.Column(db.String(100))
    version = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, inactive, decommissioned
    last_scanned = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('User', backref='owned_assets')
    vulnerabilities = db.relationship('AssetVulnerability', back_populates='asset', cascade='all, delete-orphan')
    incidents = db.relationship('IncidentAsset', back_populates='asset', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Asset {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'category': self.category,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
            'operating_system': self.operating_system,
            'version': self.version,
            'owner_id': self.owner_id,
            'location': self.location,
            'status': self.status,
            'last_scanned': self.last_scanned.isoformat() if self.last_scanned else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'owner': self.owner.username if self.owner else None,
            'vulnerabilities_count': len(self.vulnerabilities) if self.vulnerabilities else 0
        }

