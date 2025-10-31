# Quick Deployment Guide

## Adding/Updating Subdomains

### 1. Edit Configuration
```bash
# Edit subdomains.json - add or modify entries
nano subdomains.json
```

### 2. Generate Worker Code
```bash
python3 generate-worker.py
```

### 3. Deploy via CLI (Recommended)
```bash
wrangler deploy
```

That's it! Your changes are live.

## Alternative: Deploy via Dashboard

If you prefer using the Cloudflare dashboard:

1. Run steps 1-2 above
2. Go to: https://dash.cloudflare.com → Workers & Pages → illinihunt-reverse-proxy
3. Click **Edit Code**
4. Select all (Cmd+A) and delete
5. Copy entire contents of `cloudflare-worker.js`
6. Paste into editor
7. Click **Save and Deploy**

**Note:** CLI deployment is more reliable if dashboard saves don't seem to stick.

## Verify Deployment

Test root domain (shows configured subdomains):
```bash
curl https://illinihunt.org
```

Test specific subdomain:
```bash
curl -I https://core-v2.illinihunt.org
```

## Files

- **`subdomains.json`** - Edit this to add/remove subdomains
- **`generate-worker.py`** - Regenerates worker code
- **`cloudflare-worker.js`** - Auto-generated worker code
- **`wrangler.toml`** - Wrangler CLI configuration (don't edit)

## Already Configured

- Worker name: `illinihunt-reverse-proxy`
- Account ID: `e64cab2cda0c00bba0784e6cd56e36c6`
- Routes: `*.illinihunt.org/*` and `illinihunt.org/*`
- Current subdomains: 26

## Troubleshooting

**Dashboard deployment not working?**
→ Use `wrangler deploy` instead

**Need to check what's deployed?**
```bash
wrangler deployments list --name illinihunt-reverse-proxy
```

**Need to rollback?**
```bash
wrangler rollback --name illinihunt-reverse-proxy
```
