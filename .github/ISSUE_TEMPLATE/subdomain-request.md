---
name: Subdomain Request
about: Request a new subdomain or update an existing one
title: '[SUBDOMAIN] '
labels: subdomain-request
assignees: ''
---

## Subdomain Information

**Subdomain Name:** (e.g., myproject-v1)

**Bolt.host URL:** (e.g., https://my-project-abc123.bolt.host/)

**Action:** (new or update)

---

### Naming Convention

**For Landing Pages:** Use `-v1`, `-v2` suffix
Example: `myproject-v1` → `myproject-v1.illinihunt.org`

**For MVP Apps:** No suffix
Example: `myproject` → `myproject.illinihunt.org`

### Instructions:
1. Fill in your desired subdomain name (lowercase, alphanumeric, hyphens allowed)
2. Provide your full bolt.host, Vercel, or other supported platform URL
3. Specify if this is a new subdomain or an update to an existing one
4. Submit the issue

The automation will:
- Validate your request
- Create DNS record automatically
- Update the DNS configuration
- Deploy your subdomain
- Comment back with the result

Your subdomain will be available at: `https://[subdomain-name].illinihunt.org`

**Supported platforms:** bolt.host, vercel.app, netlify.app, onrender.com, fly.dev
