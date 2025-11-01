# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Automated subdomain management system for `illinihunt.org` using Cloudflare Workers and GitHub Actions. Students submit GitHub issues to request subdomains, and automation validates, deploys, and configures DNS records.

**Course:** BADM 350 (Course ID: badm_350_120255_247989)

## Key Architecture

### Issue-Driven Workflow
1. Student creates GitHub issue with subdomain request (via issue template)
2. GitHub Actions workflow triggers on issue creation/edit
3. Workflow validates user against `allowlist.txt`
4. Python script parses issue body, validates subdomain/URL
5. `subdomains.json` is updated with new mapping
6. `generate-worker.py` regenerates `cloudflare-worker.js` from config
7. `manage-dns.py` creates CNAME record via Cloudflare API
8. Wrangler deploys worker to Cloudflare
9. Changes committed to repo, success/failure comment posted to issue

### Multi-Platform Support
- **bolt.host**: Store project ID only (e.g., `"myproject": "project-abc123"`)
- **Other platforms** (Vercel, Netlify, etc.): Store full URL (e.g., `"myproject": "https://myproject.vercel.app"`)
- Worker handles both formats automatically

### Auto-Detection Feature
The `Action` field in issue template is optional. If omitted:
- Script checks if subdomain exists in `subdomains.json`
- Auto-selects `new` or `update` action
- Simplifies workflow for students updating URLs

### Subdomain Naming Convention
- **Versioned** (`-v1`, `-v2`): Pre-launch teaser campaign landing pages
- **Non-versioned**: MVP production applications
- Convention documented in README.md and issue template

## Common Commands

### Local Testing
```bash
# Test issue parser script
python3 .github/scripts/process-subdomain-request.py "$(cat <<EOF
**Subdomain Name:** test-v1
**Bolt.host URL:** https://test-project.bolt.host
EOF
)"

# Generate worker from config
python3 generate-worker.py

# Deploy worker to Cloudflare
wrangler deploy
```

### Manual Subdomain Management
```bash
# 1. Edit subdomains.json directly
nano subdomains.json

# 2. Regenerate worker code
python3 generate-worker.py

# 3. Deploy to Cloudflare
wrangler deploy

# 4. Commit changes
git add subdomains.json cloudflare-worker.js
git commit -m "Manual update: [description]"
git push
```

### DNS Management
```bash
# Create DNS record for subdomain (requires CLOUDFLARE_API_TOKEN env var)
.github/scripts/manage-dns.py create <subdomain-name>

# List all DNS records
.github/scripts/manage-dns.py list

# Delete DNS record
.github/scripts/manage-dns.py delete <subdomain-name>
```

### Bulk Operations
```bash
# Bulk add subdomains from text file
# Format: URL    subdomain@illinihunt.org (one per line)
.github/scripts/bulk-setup.py "$(cat <<'EOF'
https://project1.bolt.host    project1@illinihunt.org
https://project2.vercel.app   project2@illinihunt.org
EOF
)"
```

### Testing Workflow
```bash
# Create test issue to verify automation
gh issue create --title "Test subdomain" --label "subdomain-request" --body "**Subdomain Name:** test
**Bolt.host URL:** https://test.bolt.host"

# Monitor workflow runs
gh run list --limit 5

# View specific run details
gh run view <run-id>

# View failed run logs
gh run view <run-id> --log-failed
```

## Critical Files

### Configuration Files
- **`subdomains.json`**: Source of truth for subdomain mappings. Format:
  ```json
  {
    "comment": "Description",
    "subdomains": {
      "subdomain-name": "project-id-or-full-url"
    }
  }
  ```
- **`allowlist.txt`**: Authorized GitHub usernames (one per line, supports `#` comments)
- **`wrangler.toml`**: Cloudflare Worker config (account ID, routes)

### Generated Files
- **`cloudflare-worker.js`**: Auto-generated from `subdomains.json` via `generate-worker.py`. Never edit manually.

### Scripts
- **`generate-worker.py`**: Reads `subdomains.json`, generates `cloudflare-worker.js`
- **`.github/scripts/process-subdomain-request.py`**: Parses issue body, validates input, updates config
- **`.github/scripts/manage-dns.py`**: Creates/deletes/lists DNS records via Cloudflare API
- **`.github/scripts/bulk-setup.py`**: Bulk subdomain configuration from text lists

### Workflow
- **`.github/workflows/process-subdomain-request.yml`**: Main automation workflow
  - Concurrency control: `subdomain-request-${{ github.event.issue.number }}`
  - Requires: `issues: write`, `contents: write` permissions
  - Triggered on: `issues` (opened, edited) with `subdomain-request` label

## Important Patterns

### Cloudflare Worker Reverse Proxy
The worker intercepts requests to `*.illinihunt.org` subdomains and proxies to target URLs (bolt.host, Vercel, etc.). The root domain (`illinihunt.org`) passes through to its Vercel deployment.

### Error Handling in Workflow
Workflow uses step outputs to track success/failure:
- `check_allowlist.outputs.authorized`: Authorization status
- `process.outcome`: Validation result
- Separate comment steps for different failure modes (unauthorized, validation failed, deployment failed)

### DNS Record Management
All DNS records are CNAME records pointing to root domain (`illinihunt.org`) with Cloudflare proxy enabled (`proxied: true`). This allows the worker to intercept and route requests.

## Secrets Required

### GitHub Repository Secret
- **`CLOUDFLARE_API_TOKEN`**: Cloudflare API token with permissions:
  - Account: `Workers Scripts:Edit`
  - Zone: `illinihunt.org` → `Workers Routes:Edit`
  - Zone: `illinihunt.org` → `DNS:Edit`

### Setting Secret via CLI
```bash
gh secret set CLOUDFLARE_API_TOKEN --body "your-token-here"
```

## Development Workflow

### Adding Students to Allowlist
1. Edit `allowlist.txt`, add GitHub username (one per line)
2. Commit and push: `git add allowlist.txt && git commit -m "Add student to allowlist" && git push`
3. Students can immediately create subdomain requests

### Updating Subdomain URL
Students submit issue with same subdomain name, different URL. Script auto-detects it's an update (if `Action` field omitted).

### Removing Subdomain
1. Manually edit `subdomains.json`, remove entry
2. `python3 generate-worker.py`
3. `wrangler deploy`
4. (Optional) Delete DNS record: `.github/scripts/manage-dns.py delete <subdomain>`
5. Commit and push changes

## Troubleshooting

### Workflow Failures
- **"not authorized"**: GitHub username not in `allowlist.txt` (check exact match, case-sensitive)
- **"subdomain already exists"**: Student used `Action: new` for existing subdomain (or omit Action field)
- **"deployment failed"**: Check `CLOUDFLARE_API_TOKEN` secret, verify token permissions
- **"nothing to commit"**: Subdomain URL unchanged (not an error, but workflow exits)

### Subdomain Not Working
1. Verify DNS record exists: `.github/scripts/manage-dns.py list | grep <subdomain>`
2. Test worker directly: `curl https://<subdomain>.illinihunt.org`
3. Check Cloudflare Worker logs in dashboard
4. Wait 2-5 minutes for DNS propagation

### Worker Not Routing Correctly
- Verify `subdomains.json` has correct mapping
- Check `cloudflare-worker.js` was regenerated: `git log cloudflare-worker.js`
- Redeploy: `wrangler deploy`
- Check worker logs for request routing

## Platform-Specific Notes

### Cloudflare Workers
- Worker name: `illinihunt-reverse-proxy`
- Routes: `illinihunt.org/*` and `*.illinihunt.org/*`
- Compatibility date: `2024-10-01`
- Account ID in `wrangler.toml`

### GitHub Actions
- Workflow runs on `ubuntu-latest`
- Python 3.11, Node.js 20
- Concurrency control prevents duplicate runs per issue
- Auto-closes issues on successful deployment

### DNS Records
- All records are CNAME pointing to `illinihunt.org`
- TTL: 1 (auto)
- Proxied: true (Cloudflare proxy enabled)
- Created automatically by workflow via Cloudflare API
