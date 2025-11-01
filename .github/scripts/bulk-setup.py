#!/usr/bin/env python3
"""
Bulk setup subdomains from a list
Parses subdomain -> URL mappings and updates configuration
"""

import json
import re
import sys

def parse_subdomain_list(text):
    """Parse subdomain list from text"""

    mappings = []
    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Parse format: URL    subdomain@illinihunt.org
        # or: subdomain@illinihunt.org    URL
        parts = re.split(r'\s+', line)
        parts = [p for p in parts if p]  # Remove empty

        if len(parts) < 2:
            continue

        # Find URL and subdomain
        url = None
        subdomain = None

        for part in parts:
            if part.startswith('http'):
                url = part
            elif '@illinihunt.org' in part:
                subdomain = part.replace('@illinihunt.org', '')

        if url and subdomain:
            mappings.append({'subdomain': subdomain, 'url': url})

    return mappings

def extract_project_id(url):
    """Extract project ID from bolt.host or vercel URL"""

    # bolt.host format: https://project-id.bolt.host
    bolt_match = re.match(r'https?://([a-z0-9-]+)\.bolt\.host', url, re.IGNORECASE)
    if bolt_match:
        return bolt_match.group(1), 'bolt.host'

    # vercel format: https://project-name.vercel.app
    vercel_match = re.match(r'https?://([a-z0-9-]+)\.vercel\.app', url, re.IGNORECASE)
    if vercel_match:
        return vercel_match.group(1), 'vercel.app'

    return None, None

def main():
    """Main function"""

    if len(sys.argv) < 2:
        print("Usage: bulk-setup.py '<subdomain list>'")
        sys.exit(1)

    text = sys.argv[1]

    # Parse subdomain list
    mappings = parse_subdomain_list(text)

    if not mappings:
        print("ERROR: No valid subdomain mappings found")
        sys.exit(1)

    # Load existing config
    with open('subdomains.json', 'r') as f:
        config = json.load(f)

    subdomains = config.get('subdomains', {})

    # Process each mapping
    new_count = 0
    updated_count = 0

    for mapping in mappings:
        subdomain = mapping['subdomain']
        url = mapping['url']

        project_id, platform = extract_project_id(url)

        if not project_id:
            print(f"⚠️  Could not parse URL for {subdomain}: {url}")
            continue

        # For bolt.host, store just project ID (legacy format)
        # For other platforms, store full URL
        if platform == 'bolt.host':
            target = project_id
        else:
            target = url.rstrip('/')

        # Check if exists
        if subdomain in subdomains:
            old_value = subdomains[subdomain]
            if old_value != target:
                print(f"✏️  Update: {subdomain} ({old_value} -> {target})")
                subdomains[subdomain] = target
                updated_count += 1
            else:
                print(f"✓  Unchanged: {subdomain}")
        else:
            print(f"✅ Add: {subdomain} -> {target} ({platform})")
            subdomains[subdomain] = target
            new_count += 1

    # Save config
    config['subdomains'] = subdomains
    with open('subdomains.json', 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n📊 Summary: {new_count} added, {updated_count} updated")
    print(f"💾 Updated subdomains.json")

    # Output subdomain list for DNS creation
    print("\n📋 Subdomains to create DNS records for:")
    for mapping in mappings:
        subdomain = mapping['subdomain']
        if subdomain in subdomains:
            print(f"  - {subdomain}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
