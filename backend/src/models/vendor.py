from datetime import datetime
from .user import db

class Vendor(db.Model):
    __tablename__ = 'vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    risk_tier = db.Column(db.String(20))  # high, medium, low
    status = db.Column(db.String(20), default='active')  # active, inactive, terminated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assessments = db.relationship('VendorAssessment', back_populates='vendor', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Vendor {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'website': self.website,
            'risk_tier': self.risk_tier,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class VendorAssessment(db.Model):
    __tablename__ = 'vendor_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    assessment_type = db.Column(db.String(50))  # security, privacy, operational
    score = db.Column(db.Integer)  # 0-100
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    assessor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    findings = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    next_assessment_date = db.Column(db.Date)
    
    # Relationships
    vendor = db.relationship('Vendor', back_populates='assessments')
    assessor = db.relationship('User', backref='vendor_assessments')

    def __repr__(self):
        return f'<VendorAssessment {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'assessment_type': self.assessment_type,
            'score': self.score,
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'assessor_id': self.assessor_id,
            'findings': self.findings,
            'recommendations': self.recommendations,
            'next_assessment_date': self.next_assessment_date.isoformat() if self.next_assessment_date else None,
            'vendor': self.vendor.name if self.vendor else None,
            'assessor': self.assessor.username if self.assessor else None
        }

