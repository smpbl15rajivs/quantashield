from datetime import datetime
from .user import db

class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))  # critical, high, medium, low
    status = db.Column(db.String(20), default='open')  # open, investigating, contained, resolved, closed
    category = db.Column(db.String(50))  # malware, phishing, data_breach, etc.
    source = db.Column(db.String(100))  # how the incident was detected
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Relationships
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_incidents')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_incidents')
    timeline = db.relationship('IncidentTimeline', back_populates='incident', cascade='all, delete-orphan')
    assets = db.relationship('IncidentAsset', back_populates='incident', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Incident {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'status': self.status,
            'category': self.category,
            'source': self.source,
            'assigned_to': self.assigned_to,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'assignee': self.assignee.username if self.assignee else None,
            'creator': self.creator.username if self.creator else None
        }

class IncidentTimeline(db.Model):
    __tablename__ = 'incident_timeline'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    incident = db.relationship('Incident', back_populates='timeline')
    performer = db.relationship('User', backref='incident_actions')

    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'action': self.action,
            'description': self.description,
            'performed_by': self.performed_by,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'performer': self.performer.username if self.performer else None
        }

class IncidentAsset(db.Model):
    __tablename__ = 'incident_assets'
    
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), primary_key=True)
    impact_level = db.Column(db.String(20))  # affected, compromised, at_risk
    
    # Relationships
    incident = db.relationship('Incident', back_populates='assets')
    asset = db.relationship('Asset', back_populates='incidents')

    def to_dict(self):
        return {
            'incident_id': self.incident_id,
            'asset_id': self.asset_id,
            'impact_level': self.impact_level,
            'asset': self.asset.to_dict() if self.asset else None
        }

