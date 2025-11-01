#!/usr/bin/env python3
"""
Generate Cloudflare Worker code from subdomain configuration

Usage:
    python3 generate-worker.py

This reads subdomains.json and generates cloudflare-worker.js
"""

import json

def generate_worker_code(subdomain_map):
    """Generate the complete Cloudflare Worker JavaScript code"""

    # Convert subdomain map to JavaScript object literal
    # Supports both project IDs (for bolt.host) and full URLs
    js_map_entries = []
    for subdomain, target in subdomain_map.items():
        # If target looks like a URL, use it as-is, otherwise assume bolt.host project ID
        if target.startswith('http://') or target.startswith('https://'):
            js_map_entries.append(f'  "{subdomain}": "{target}"')
        else:
            # Legacy format: just project ID, assume bolt.host
            js_map_entries.append(f'  "{subdomain}": "https://{target}.bolt.host"')

    js_map = ",\n".join(js_map_entries) if js_map_entries else "  // No subdomains configured yet"

    worker_code = f'''/**
 * Cloudflare Worker - Reverse Proxy for illinihunt.org subdomains
 * Maps subdomains to bolt.host hosted sites
 *
 * AUTO-GENERATED from subdomains.json
 * Run: python3 generate-worker.py
 */

// SUBDOMAIN CONFIGURATION
const SUBDOMAIN_MAP = {{
{js_map}
}};

/**
 * Main request handler
 */
async function handleRequest(request) {{
  const url = new URL(request.url);
  const hostname = url.hostname;

  // Extract subdomain from hostname
  const subdomain = hostname.split('.')[0];
  const isRootDomain = hostname === 'illinihunt.org' || hostname === 'www.illinihunt.org';

  // Log for debugging
  console.log(`Request: ${{hostname}} -> Subdomain: ${{subdomain}}`);

  // Let root domain pass through (don't intercept)
  // This allows illinihunt.org to be handled by its Vercel deployment
  if (isRootDomain) {{
    return fetch(request);
  }}

  // Check if subdomain is mapped
  const targetBase = SUBDOMAIN_MAP[subdomain];

  if (!targetBase) {{
    return new Response(`Subdomain "${{subdomain}}" not configured\\nAvailable: ${{Object.keys(SUBDOMAIN_MAP).join(', ')}}`, {{
      status: 404,
      headers: {{ 'Content-Type': 'text/plain' }}
    }});
  }}

  // Build target URL
  // targetBase can be either a full URL or a project ID (legacy)
  let targetUrl;
  if (targetBase.startsWith('http://') || targetBase.startsWith('https://')) {{
    // Full URL format
    const baseUrl = new URL(targetBase);
    targetUrl = `${{baseUrl.origin}}${{url.pathname}}${{url.search}}`;
  }} else {{
    // Legacy project ID format (assume bolt.host)
    targetUrl = `https://${{targetBase}}.bolt.host${{url.pathname}}${{url.search}}`;
  }}

  // Create new request to target
  const modifiedRequest = new Request(targetUrl, {{
    method: request.method,
    headers: request.headers,
    body: request.body,
    redirect: 'follow'
  }});

  // Fetch from target
  const response = await fetch(modifiedRequest);

  // Create response with modified headers
  const modifiedResponse = new Response(response.body, response);

  // Update headers for proper proxying
  modifiedResponse.headers.set('Access-Control-Allow-Origin', '*');
  modifiedResponse.headers.delete('X-Frame-Options');

  return modifiedResponse;
}}

/**
 * Cloudflare Worker entry point
 */
addEventListener('fetch', event => {{
  event.respondWith(handleRequest(event.request));
}});
'''
    return worker_code

def main():
    """Main function"""

    # Read configuration
    try:
        with open('subdomains.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: subdomains.json not found")
        print("Create it with format: {\"subdomains\": {\"sub\": \"bolt-id\"}}")
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in subdomains.json: {e}")
        return 1

    subdomain_map = config.get('subdomains', {})

    # Generate worker code
    worker_code = generate_worker_code(subdomain_map)

    # Write to file
    with open('cloudflare-worker.js', 'w') as f:
        f.write(worker_code)

    # Print summary
    print("✅ Generated cloudflare-worker.js")
    print(f"📊 Configured subdomains: {len(subdomain_map)}")

    if subdomain_map:
        print("\\nSubdomains:")
        for subdomain, target in subdomain_map.items():
            # Display target correctly (full URL or project ID)
            if target.startswith('http://') or target.startswith('https://'):
                print(f"  • {subdomain}.illinihunt.org -> {target}")
            else:
                print(f"  • {subdomain}.illinihunt.org -> {target}.bolt.host")
    else:
        print("⚠️  No subdomains configured yet")
        print("   Add entries to subdomains.json")

    print("\\n📋 Next steps:")
    print("1. Copy cloudflare-worker.js content")
    print("2. Go to Cloudflare Workers dashboard")
    print("3. Edit your worker and paste the code")
    print("4. Save and Deploy")

    return 0

if __name__ == '__main__':
    exit(main())