#!/usr/bin/env python3
"""
Manage Cloudflare DNS records for illinihunt.org subdomains

Creates/updates CNAME records pointing to illinihunt.org (proxied)
"""

import json
import os
import sys
import urllib.request
import urllib.error


ZONE_NAME = "illinihunt.org"
API_BASE = "https://api.cloudflare.com/client/v4"


def make_api_request(endpoint, method="GET", data=None):
    """Make authenticated request to Cloudflare API"""

    api_token = os.environ.get('CLOUDFLARE_API_TOKEN')
    if not api_token:
        raise ValueError("CLOUDFLARE_API_TOKEN environment variable not set")

    url = f"{API_BASE}{endpoint}"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    request_data = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=request_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"API Error: {e.code} - {error_body}")
        raise


def get_zone_id():
    """Get zone ID for illinihunt.org"""

    response = make_api_request(f"/zones?name={ZONE_NAME}")

    if not response.get('success'):
        raise ValueError(f"Failed to get zone ID: {response.get('errors')}")

    zones = response.get('result', [])
    if not zones:
        raise ValueError(f"Zone {ZONE_NAME} not found")

    return zones[0]['id']


def get_dns_record(zone_id, subdomain):
    """Check if DNS record already exists"""

    full_name = f"{subdomain}.{ZONE_NAME}"
    response = make_api_request(f"/zones/{zone_id}/dns_records?type=CNAME&name={full_name}")

    if not response.get('success'):
        return None

    records = response.get('result', [])
    return records[0] if records else None


def create_dns_record(zone_id, subdomain):
    """Create CNAME record for subdomain"""

    full_name = f"{subdomain}.{ZONE_NAME}"

    # Check if record already exists
    existing = get_dns_record(zone_id, subdomain)
    if existing:
        print(f"DNS record already exists for {full_name}")
        return existing['id']

    # Create CNAME record pointing to root domain (proxied)
    data = {
        'type': 'CNAME',
        'name': subdomain,
        'content': ZONE_NAME,
        'ttl': 1,  # Automatic
        'proxied': True  # Orange cloud
    }

    response = make_api_request(f"/zones/{zone_id}/dns_records", method="POST", data=data)

    if not response.get('success'):
        errors = response.get('errors', [])
        raise ValueError(f"Failed to create DNS record: {errors}")

    record_id = response['result']['id']
    print(f"✅ Created DNS record: {full_name} -> {ZONE_NAME} (proxied)")
    return record_id


def delete_dns_record(zone_id, subdomain):
    """Delete DNS record for subdomain"""

    existing = get_dns_record(zone_id, subdomain)
    if not existing:
        print(f"DNS record does not exist for {subdomain}.{ZONE_NAME}")
        return

    record_id = existing['id']
    response = make_api_request(f"/zones/{zone_id}/dns_records/{record_id}", method="DELETE")

    if not response.get('success'):
        errors = response.get('errors', [])
        raise ValueError(f"Failed to delete DNS record: {errors}")

    print(f"✅ Deleted DNS record: {subdomain}.{ZONE_NAME}")


def main():
    """Main function"""

    if len(sys.argv) < 3:
        print("Usage: manage-dns.py <action> <subdomain>")
        print("Actions: create, delete")
        sys.exit(1)

    action = sys.argv[1].lower()
    subdomain = sys.argv[2]

    try:
        # Get zone ID
        print(f"Looking up zone ID for {ZONE_NAME}...")
        zone_id = get_zone_id()
        print(f"Zone ID: {zone_id}")

        # Perform action
        if action == 'create':
            create_dns_record(zone_id, subdomain)
        elif action == 'delete':
            delete_dns_record(zone_id, subdomain)
        else:
            print(f"Unknown action: {action}")
            sys.exit(1)

        print("SUCCESS")
        return 0

    except Exception as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
