from datetime import datetime
from .user import db

class Policy(db.Model):
    __tablename__ = 'policies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    version = db.Column(db.String(20), default='1.0')
    status = db.Column(db.String(20), default='draft')  # draft, approved, published, archived
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    effective_date = db.Column(db.Date)
    review_date = db.Column(db.Date)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_policies')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_policies')
    acknowledgments = db.relationship('PolicyAcknowledgment', back_populates='policy', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Policy {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'content': self.content,
            'version': self.version,
            'status': self.status,
            'created_by': self.created_by,
            'approved_by': self.approved_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'creator': self.creator.username if self.creator else None,
            'approver': self.approver.username if self.approver else None
        }

class PolicyAcknowledgment(db.Model):
    __tablename__ = 'policy_acknowledgments'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), primary_key=True)
    acknowledged_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='policy_acknowledgments')
    policy = db.relationship('Policy', back_populates='acknowledgments')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'policy_id': self.policy_id,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            'user': self.user.username if self.user else None,
            'policy': self.policy.title if self.policy else None
        }

