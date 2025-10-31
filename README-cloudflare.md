# Cloudflare Worker - Subdomain Reverse Proxy

Easy-to-update reverse proxy for `illinihunt.org` subdomains pointing to bolt.net sites.

## Quick Start: Adding a New Subdomain

### 1. Edit `subdomains.json`

```json
{
  "comment": "Add your subdomain mappings here",
  "subdomains": {
    "demo": "demo-project-abc123",
    "portfolio": "portfolio-xyz789"
  }
}
```

**Format:** `"subdomain": "bolt-project-id"`

To get your bolt project ID, look at your bolt.net URL:
- URL: `https://your-project-id.bolt.new`
- Use: `your-project-id`

### 2. Generate Worker Code

```bash
python3 generate-worker.py
```

This creates/updates `cloudflare-worker.js` with your subdomains.

### 3. Add DNS Record in Cloudflare

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Select **illinihunt.org**
3. Go to **DNS** → **Records**
4. Click **Add record**:
   - **Type:** CNAME
   - **Name:** your-subdomain (e.g., `demo`)
   - **Target:** `illinihunt.org`
   - **Proxy status:** Proxied ☁️ (orange cloud)
5. Click **Save**

### 4. Update Worker in Cloudflare

1. Go to **Workers & Pages** in Cloudflare dashboard
2. Click your worker (find it in the list)
3. Click **Edit Code** or **Quick Edit**
4. Select all existing code (Cmd+A) and delete
5. Open `cloudflare-worker.js` from this folder
6. Copy entire content (Cmd+A, Cmd+C)
7. Paste into Cloudflare editor (Cmd+V)
8. Click **Save and Deploy**

### 5. Test

Wait 1-2 minutes, then visit: `https://your-subdomain.illinihunt.org`

## Files

- **`subdomains.json`** - Easy config file (edit this!)
- **`generate-worker.py`** - Generates worker code from config
- **`cloudflare-worker.js`** - Generated worker code (copy to Cloudflare)
- **`subdomain-mappings.md`** - Detailed documentation
- **`README-cloudflare.md`** - This file

## Workflow Summary

```
Edit subdomains.json → Run generate-worker.py → Copy cloudflare-worker.js → Paste in Cloudflare → Deploy
```

## Example `subdomains.json`

```json
{
  "subdomains": {
    "student1": "project-abc123",
    "student2": "project-def456",
    "demo": "demo-project-xyz",
    "syllabus": "syllabus-site-123"
  }
}
```

This creates:
- `student1.illinihunt.org` → `project-abc123.bolt.new`
- `student2.illinihunt.org` → `project-def456.bolt.new`
- `demo.illinihunt.org` → `demo-project-xyz.bolt.new`
- `syllabus.illinihunt.org` → `syllabus-site-123.bolt.new`

## Troubleshooting

### Can't find your Cloudflare Worker?

1. Go to Cloudflare dashboard
2. Click **Workers & Pages** in left sidebar
3. Look for a worker with a route containing `illinihunt.org`
4. If you don't see one, you may need to create a new worker

### Creating a new worker (if needed):

1. Click **Create Application** → **Create Worker**
2. Name it `illinihunt-proxy` (or similar)
3. Click **Deploy**
4. Go to **Settings** → **Triggers**
5. Add route: `*.illinihunt.org/*`
6. Return to worker and edit code with your generated code

### "Subdomain not configured" error?

- Check subdomain is in `subdomains.json`
- Re-run `generate-worker.py`
- Re-deploy worker code
- Check spelling matches DNS record exactly

### Still not working?

Check:
1. DNS record is **Proxied** (orange cloud ☁️)
2. Worker route includes `*.illinihunt.org/*`
3. Bolt.net project ID is correct (test by visiting `project-id.bolt.new` directly)
4. Wait 2-5 minutes for DNS propagation

## Need Help?

See `subdomain-mappings.md` for detailed troubleshooting and configuration options.
