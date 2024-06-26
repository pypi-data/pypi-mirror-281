# test_app/models.py
from flask_tenants import BaseTenant, BaseDomain, db


class Tenant(BaseTenant):
    __tablename__ = 'tenants'
    phone_number = db.Column(db.String(20), nullable=True)  # Additional field
    address = db.Column(db.String(255), nullable=True)  # Additional field


class Domain(BaseDomain):
    __tablename__ = 'domains'
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)  # Ensure correct foreign key

    def __repr__(self):
        return f'<Domain {self.domain_name} (Primary: {self.is_primary})>'
