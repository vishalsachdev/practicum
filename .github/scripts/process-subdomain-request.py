#!/usr/bin/env python3
"""
Process subdomain request from GitHub issue

Parses issue body, validates input, and updates subdomains.json
"""

import json
import re
import sys
from pathlib import Path


def parse_issue_body(body):
    """Extract subdomain and URL from issue body"""

    subdomain_match = re.search(r'\*\*Subdomain Name:\*\*\s*(.+)', body, re.IGNORECASE)
    url_match = re.search(r'\*\*Bolt\.host URL:\*\*\s*(.+)', body, re.IGNORECASE)
    action_match = re.search(r'\*\*Action:\*\*\s*(.+)', body, re.IGNORECASE)

    if not subdomain_match or not url_match:
        return None, None, None

    subdomain = subdomain_match.group(1).strip()
    url = url_match.group(1).strip()
    action = action_match.group(1).strip().lower() if action_match else 'new'

    return subdomain, url, action


def validate_subdomain(subdomain):
    """Validate subdomain name format"""

    # Must be lowercase alphanumeric with hyphens
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', subdomain):
        return False, "Subdomain must be lowercase alphanumeric with hyphens (start and end with alphanumeric)"

    # Reasonable length
    if len(subdomain) > 50:
        return False, "Subdomain too long (max 50 characters)"

    return True, ""


def validate_bolt_url(url):
    """Validate and extract target URL (supports bolt.host, vercel.app, etc.)"""

    # Match bolt.host or bolt.new URLs
    bolt_match = re.match(r'https?://([a-z0-9-]+)\.bolt\.(host|new)/?', url, re.IGNORECASE)
    if bolt_match:
        project_id = bolt_match.group(1)
        return project_id, ""

    # Match vercel.app URLs (store as full URL)
    vercel_match = re.match(r'(https?://[a-z0-9-]+\.vercel\.app)/?', url, re.IGNORECASE)
    if vercel_match:
        full_url = vercel_match.group(1)
        return full_url, ""

    # Match other common platforms (netlify, render, fly.io, etc.)
    other_match = re.match(r'(https?://[a-z0-9-]+\.(netlify\.app|onrender\.com|fly\.dev))/?', url, re.IGNORECASE)
    if other_match:
        full_url = other_match.group(1)
        return full_url, ""

    return None, "Invalid URL format. Supported: bolt.host, vercel.app, netlify.app, onrender.com, fly.dev"


def update_subdomains_config(subdomain, project_id, action):
    """Update subdomains.json with new/updated subdomain"""

    config_file = Path('subdomains.json')

    if not config_file.exists():
        return False, "subdomains.json not found"

    with open(config_file, 'r') as f:
        config = json.load(f)

    subdomains = config.get('subdomains', {})

    # Check if subdomain exists
    exists = subdomain in subdomains

    if action == 'new' and exists:
        return False, f"Subdomain '{subdomain}' already exists. Use 'update' action to modify it."

    if action == 'update' and not exists:
        return False, f"Subdomain '{subdomain}' does not exist. Use 'new' action to create it."

    # Update subdomain
    old_value = subdomains.get(subdomain)
    subdomains[subdomain] = project_id
    config['subdomains'] = subdomains

    # Write back
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    action_msg = f"Updated '{subdomain}' from {old_value} to {project_id}" if action == 'update' else f"Added '{subdomain}' -> {project_id}"
    return True, action_msg


def main():
    """Main function"""

    if len(sys.argv) < 2:
        print("ERROR: Missing issue body")
        sys.exit(1)

    issue_body = sys.argv[1]

    # Parse issue
    subdomain, url, action = parse_issue_body(issue_body)

    if not subdomain or not url:
        print("ERROR: Could not parse subdomain or URL from issue body")
        print("Make sure you filled in both 'Subdomain Name' and 'Bolt.host URL' fields")
        sys.exit(1)

    # Validate subdomain
    valid, error = validate_subdomain(subdomain)
    if not valid:
        print(f"ERROR: Invalid subdomain: {error}")
        sys.exit(1)

    # Validate and extract bolt URL
    project_id, error = validate_bolt_url(url)
    if not project_id:
        print(f"ERROR: Invalid URL: {error}")
        sys.exit(1)

    # Update config
    success, message = update_subdomains_config(subdomain, project_id, action)

    if not success:
        print(f"ERROR: {message}")
        sys.exit(1)

    # Success
    print(f"SUCCESS: {message}")
    print(f"SUBDOMAIN: {subdomain}")
    print(f"PROJECT_ID: {project_id}")
    print(f"URL: https://{subdomain}.illinihunt.org")

    return 0


if __name__ == '__main__':
    sys.exit(main())
