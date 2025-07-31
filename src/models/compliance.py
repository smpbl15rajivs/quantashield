from datetime import datetime
from .user import db

class ComplianceFramework(db.Model):
    __tablename__ = 'compliance_frameworks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(20))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    controls = db.relationship('Control', back_populates='framework', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ComplianceFramework {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'is_active': self.is_active
        }

class Control(db.Model):
    __tablename__ = 'controls'
    
    id = db.Column(db.Integer, primary_key=True)
    framework_id = db.Column(db.Integer, db.ForeignKey('compliance_frameworks.id'))
    control_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    
    # Relationships
    framework = db.relationship('ComplianceFramework', back_populates='controls')
    assessments = db.relationship('ControlAssessment', back_populates='control', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Control {self.control_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'framework_id': self.framework_id,
            'control_id': self.control_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'framework': self.framework.name if self.framework else None
        }

class ControlAssessment(db.Model):
    __tablename__ = 'control_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
    status = db.Column(db.String(20))  # compliant, non_compliant, partially_compliant, not_assessed
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    assessor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    evidence = db.Column(db.Text)
    remediation_plan = db.Column(db.Text)
    next_assessment_date = db.Column(db.Date)
    
    # Relationships
    control = db.relationship('Control', back_populates='assessments')
    assessor = db.relationship('User', backref='control_assessments')

    def __repr__(self):
        return f'<ControlAssessment {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'control_id': self.control_id,
            'status': self.status,
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'assessor_id': self.assessor_id,
            'evidence': self.evidence,
            'remediation_plan': self.remediation_plan,
            'next_assessment_date': self.next_assessment_date.isoformat() if self.next_assessment_date else None,
            'control': self.control.to_dict() if self.control else None,
            'assessor': self.assessor.username if self.assessor else None
        }

