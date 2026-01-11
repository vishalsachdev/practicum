#!/bin/bash
# Create CNAME record for agentlab.illinihunt.org → vishalsachdev.github.io

if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "Error: CLOUDFLARE_API_TOKEN environment variable not set"
    echo "Usage: export CLOUDFLARE_API_TOKEN='your-token' && ./create-agentlab-dns.sh"
    exit 1
fi

python3 <<'SCRIPT'
import json
import os
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

# Get zone ID
print("Getting zone ID for illinihunt.org...")
response = make_api_request(f"/zones?name={ZONE_NAME}")
if not response.get('success'):
    raise ValueError(f"Failed to get zone ID: {response.get('errors')}")
zones = response.get('result', [])
if not zones:
    raise ValueError(f"Zone {ZONE_NAME} not found")
zone_id = zones[0]['id']
print(f"✓ Zone ID: {zone_id}")

# Check if record already exists
full_name = f"agentlab.{ZONE_NAME}"
print(f"\nChecking if {full_name} already exists...")
response = make_api_request(f"/zones/{zone_id}/dns_records?type=CNAME&name={full_name}")
existing_records = response.get('result', [])

if existing_records:
    print(f"⚠️  Record already exists:")
    for record in existing_records:
        print(f"   ID: {record['id']}")
        print(f"   Type: {record['type']}")
        print(f"   Target: {record['content']}")
        print(f"   Proxied: {record['proxied']}")
    print("\nSkipping creation.")
    exit(0)

# Create the CNAME record
print(f"\nCreating CNAME record for {full_name}...")
dns_data = {
    "type": "CNAME",
    "name": "agentlab",
    "content": "vishalsachdev.github.io",
    "ttl": 1,  # Auto
    "proxied": False,  # DNS only (gray cloud)
    "comment": "GitHub Pages for Agent Lab"
}

print(f"\nRecord details:")
print(f"  Type: CNAME")
print(f"  Name: agentlab.illinihunt.org")
print(f"  Target: vishalsachdev.github.io")
print(f"  Proxied: False (DNS only)")
print(f"  TTL: Auto")

response = make_api_request(f"/zones/{zone_id}/dns_records", method="POST", data=dns_data)
if response.get('success'):
    print(f"\n✅ Successfully created CNAME record!")
    result = response.get('result', {})
    print(f"   ID: {result.get('id')}")
    print(f"   Name: {result.get('name')}")
    print(f"   Content: {result.get('content')}")
    print(f"   Proxied: {result.get('proxied')}")
else:
    print(f"\n❌ Failed to create record: {response.get('errors')}")
    exit(1)

SCRIPT

