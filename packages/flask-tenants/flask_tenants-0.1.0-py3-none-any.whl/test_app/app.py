# app.py
from flask import Flask, g, request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_tenants import init_app as tenants_init_app, create_tenancy, create_tenant, get_tenant, update_tenant, \
    delete_tenant, db
from test_app.models import Tenant, Domain  # Use custom models

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
app.config.from_object('test_app.config.DefaultConfig')
migrate = Migrate(app, db)

tenants_init_app(app, tenant_model=Tenant, domain_model=Domain)
tenancy = create_tenancy(app, db, tenant_url_prefix='/_tenant')

public_bp = tenancy.create_public_blueprint('public')
tenant_bp = tenancy.create_tenant_blueprint('tenant')


@public_bp.route('/')
def public_index():
    return 'Welcome to the public index page!'


@public_bp.route('/test')
def public_test():
    return 'Never gonna give you up, never gonna let you down, never gonna run around and desert you.'


@public_bp.route('/create_tenant', methods=['POST'])
def create_tenant_route():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input data"}), 400

    try:
        tenant = create_tenant(data)
        return jsonify({"message": f"Tenant {tenant.name} created successfully", "tenant": {
            "id": tenant.id,
            "name": tenant.name,
            "phone_number": tenant.phone_number,
            "address": tenant.address
        }}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@public_bp.route('/get_tenant/<int:tenant_id>', methods=['GET'])
def get_tenant_route(tenant_id):
    try:
        tenant = get_tenant(tenant_id)
        if not tenant:
            return jsonify({"error": "Tenant not found"}), 404
        return jsonify(
            {"id": tenant.id, "name": tenant.name, "phone_number": tenant.phone_number, "address": tenant.address}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@public_bp.route('/update_tenant/<int:tenant_id>', methods=['PUT'])
def update_tenant_route(tenant_id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input data"}), 400

    try:
        tenant = update_tenant(tenant_id, data)
        return jsonify({
            "message": f"Tenant {tenant.name} updated successfully",
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "phone_number": tenant.phone_number,
                "address": tenant.address
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@public_bp.route('/delete_tenant/<int:tenant_id>', methods=['DELETE'])
def delete_tenant_route(tenant_id):
    try:
        success = delete_tenant(tenant_id)
        if success:
            return jsonify({"message": "Tenant deleted successfully"}), 200
        else:
            return jsonify({"error": "Tenant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Define routes for tenant blueprint
@tenant_bp.route('/test')
def tenant_test():
    tenant = g.tenant if hasattr(g, 'tenant') else 'unknown'
    return f'Welcome to the tenant index page for {tenant}!'


@tenant_bp.route('/woah')
def tenant_woah():
    return (
        "We're no strangers to love, "
        "You know the rules and so do I. "
        "A full commitment's what I'm thinking of, "
        "You wouldn't get this from any other guy."
    )


app.register_blueprint(public_bp)
app.register_blueprint(tenant_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
