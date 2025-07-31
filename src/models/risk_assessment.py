from datetime import datetime
from .user import db

class RiskFactor(db.Model):
    __tablename__ = 'risk_factors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # technical, operational, compliance, etc.
    weight = db.Column(db.Numeric(3, 2), default=1.0)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    assessments = db.relationship('RiskAssessment', back_populates='risk_factor', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<RiskFactor {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'weight': float(self.weight) if self.weight else None,
            'description': self.description,
            'is_active': self.is_active
        }

class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    risk_factor_id = db.Column(db.Integer, db.ForeignKey('risk_factors.id'))
    score = db.Column(db.Integer)  # 0-100
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    assessor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notes = db.Column(db.Text)
    
    # Relationships
    asset = db.relationship('Asset', backref='risk_assessments')
    risk_factor = db.relationship('RiskFactor', back_populates='assessments')
    assessor = db.relationship('User', backref='risk_assessments')

    def __repr__(self):
        return f'<RiskAssessment {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'risk_factor_id': self.risk_factor_id,
            'score': self.score,
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'assessor_id': self.assessor_id,
            'notes': self.notes,
            'asset': self.asset.name if self.asset else None,
            'risk_factor': self.risk_factor.name if self.risk_factor else None,
            'assessor': self.assessor.username if self.assessor else None
        }

class SecurityScorecard(db.Model):
    __tablename__ = 'security_scorecards'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_unit = db.Column(db.String(100))
    overall_score = db.Column(db.Integer)  # 0-100
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    factors = db.Column(db.JSON)  # Store individual factor scores

    def __repr__(self):
        return f'<SecurityScorecard {self.organization_unit}>'

    def to_dict(self):
        return {
            'id': self.id,
            'organization_unit': self.organization_unit,
            'overall_score': self.overall_score,
            'calculated_at': self.calculated_at.isoformat() if self.calculated_at else None,
            'factors': self.factors
        }

