# Illinihunt.org Subdomain Mappings

## Current Subdomains

| Subdomain | Full URL | Bolt.net Project ID | Status | Notes |
|-----------|----------|---------------------|--------|-------|
| example | example.illinihunt.org | example-project-id | Active | Example entry |
| | | | | |
| | | | | |

## How to Add New Subdomains

### Step 1: Get Bolt.net Project ID
1. Go to your bolt.net site
2. Look at the URL: `https://YOUR-PROJECT-ID.bolt.new`
3. Copy the `YOUR-PROJECT-ID` part

### Step 2: Add DNS Record in Cloudflare
1. Go to Cloudflare dashboard
2. Select **illinihunt.org** domain
3. Go to **DNS** > **Records**
4. Click **Add record**
5. Settings:
   - Type: `CNAME`
   - Name: `your-subdomain` (e.g., `demo`)
   - Target: `illinihunt.org` (or your worker route)
   - Proxy status: **Proxied** (orange cloud)
6. Save

### Step 3: Update Cloudflare Worker Code
1. Open `cloudflare-worker.js` in this folder
2. Find the `SUBDOMAIN_MAP` object
3. Add your entry:
   ```javascript
   const SUBDOMAIN_MAP = {
     "your-subdomain": "your-bolt-project-id",
     // ... other entries
   };
   ```
4. Copy the entire file content

### Step 4: Deploy to Cloudflare
1. Go to Cloudflare dashboard
2. Navigate to **Workers & Pages**
3. Click on your worker (likely named something like `illinihunt-proxy`)
4. Click **Edit Code** or **Quick Edit**
5. Paste the entire updated code
6. Click **Save and Deploy**

### Step 5: Test
1. Wait 1-2 minutes for deployment
2. Visit `your-subdomain.illinihunt.org`
3. Should load your bolt.net site

## Troubleshooting

### Subdomain not working?
- Check DNS record is **Proxied** (orange cloud)
- Check worker is deployed and active
- Check subdomain spelling matches exactly in both DNS and worker code
- Check bolt.net project ID is correct
- View worker logs in Cloudflare dashboard for errors

### "Subdomain not configured" error?
- Subdomain is not in SUBDOMAIN_MAP
- Check spelling matches DNS record exactly

### Cloudflare "1xxx" errors?
- Usually DNS or routing issues
- Verify worker route includes `*illinihunt.org/*`
- Check worker is assigned to the route

## Quick Reference

### Worker Dashboard Location
Cloudflare Dashboard > Workers & Pages > [Your Worker Name]

### DNS Dashboard Location
Cloudflare Dashboard > illinihunt.org > DNS > Records

### Worker Routes
Should include route: `*illinihunt.org/*` or `*.illinihunt.org/*`
