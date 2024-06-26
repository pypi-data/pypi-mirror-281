import requests
import random
import json

BASE_URL = "http://local.test:5000"


def generate_random_tenant():
    number = random.randint(1000, 9999)
    name = f"tenant{number}"
    domain = f"{name}.local.test"
    phone = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    address = f"{random.randint(100, 999)} Example St, City, Country"
    return {
        "name": name,
        "domain_name": domain,
        "phone_number": phone,
        "address": address
    }


def create_tenant(tenant):
    try:
        response = requests.post(f"{BASE_URL}/create_tenant", json=tenant)
        response.raise_for_status()
        tenant_data = response.json().get('tenant')  # Ensure 'tenant' key exists in response
        if tenant_data:
            print(f"Created Tenant: ID={tenant_data['id']}, Name={tenant_data['name']}, "
                  f"Phone={tenant_data['phone_number']}, Address={tenant_data['address']}")
            return tenant_data
        else:
            raise ValueError("Failed to create tenant: Response does not contain 'tenant' key")
    except requests.RequestException as e:
        print(f"Error creating tenant {tenant['name']}: {e}")
    except ValueError as ve:
        print(str(ve))


def get_tenant(tenant_id):
    try:
        response = requests.get(f"{BASE_URL}/get_tenant/{tenant_id}")
        response.raise_for_status()
        tenant_data = response.json()
        print(f"Retrieved Tenant: ID={tenant_data['id']}, Name={tenant_data['name']}, "
              f"Phone={tenant_data['phone_number']}, Address={tenant_data['address']}")
        return tenant_data
    except requests.RequestException as e:
        print(f"Error retrieving tenant with ID {tenant_id}: {e}")


def update_tenant(tenant_id, update_fields):
    try:
        response = requests.put(f"{BASE_URL}/update_tenant/{tenant_id}", json=update_fields)
        response.raise_for_status()
        response_data = response.json()
        tenant_data = response_data.get('tenant')  # Ensure 'tenant' key exists in response
        if tenant_data:
            print(f"Updated Tenant: ID={tenant_data['id']}, Name={tenant_data['name']}, "
                  f"Phone={tenant_data['phone_number']}, Address={tenant_data['address']}")
            return tenant_data
        else:
            raise ValueError("Failed to update tenant: Response does not contain 'tenant' key")
    except requests.RequestException as e:
        print(f"Error updating tenant with ID {tenant_id}: {e}")
    except ValueError as ve:
        print(str(ve))


def delete_tenant(tenant_id):
    try:
        response = requests.delete(f"{BASE_URL}/delete_tenant/{tenant_id}")
        response.raise_for_status()
        print(f"Deleted Tenant: ID={tenant_id}")
    except requests.RequestException as e:
        print(f"Error deleting tenant with ID {tenant_id}: {e}")


if __name__ == "__main__":
    # Generate random tenants
    tenants = [generate_random_tenant(), generate_random_tenant()]

    created_tenants = []

    # Create tenants
    for tenant in tenants:
        created_tenant = create_tenant(tenant)
        if created_tenant:
            created_tenants.append(created_tenant)

    # Read tenants
    for tenant in created_tenants:
        get_tenant(tenant['id'])

    # Update tenants
    updated_tenants = []
    for tenant in created_tenants:
        new_name = f"{tenant['name']}_updated"
        new_phone = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        new_address = f"{random.randint(100, 999)} Updated St, City, Country"
        update_fields = {
            "name": new_name,
            "phone_number": new_phone,
            "address": new_address
        }
        updated_tenant = update_tenant(tenant['id'], update_fields)
        if updated_tenant:
            updated_tenants.append(updated_tenant)

    # Delete tenants
    for tenant in updated_tenants:
        delete_tenant(tenant['id'])
