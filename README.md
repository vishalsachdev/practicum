# Illinihunt.org Subdomain Management

Automated subdomain management system for `illinihunt.org` using Cloudflare Workers and GitHub Actions.

Students can request subdomains by creating a GitHub issue, and the system automatically validates, configures, and deploys their subdomain.

## For Students

### How to Request a Subdomain

1. **Create your bolt.host site** and note the URL (e.g., `https://my-project-abc123.bolt.host/`)

2. **Create a GitHub Issue** using the "Subdomain Request" template:
   - Click **Issues** → **New Issue**
   - Select **Subdomain Request** template
   - Fill in:
     - **Subdomain Name:** Your desired subdomain (e.g., `myproject-v1`)
     - **Bolt.host URL:** Your full bolt.host URL
     - **Action:** `new` (for first-time) or `update` (to change URL)
   - Submit the issue

3. **Wait for automation** (usually 1-2 minutes):
   - The system checks if you're authorized
   - Validates your request
   - Creates DNS record automatically
   - Deploys your subdomain
   - Comments back with status

4. **Your subdomain is live!**
   - Access at: `https://[your-subdomain].illinihunt.org`
   - DNS propagation may take 2-5 minutes

### Subdomain Naming Rules

- Lowercase alphanumeric characters and hyphens only
- Must start and end with alphanumeric character
- Maximum 50 characters
- Examples: `myproject-v1`, `student-portfolio`, `demo-site`

### Naming Convention for Student Startups

**Version Suffixes (`-v1`, `-v2`):**
- Used for **landing pages** showcasing your startup concept
- Example: `moneynova-v1.illinihunt.org` → Landing page for MoneyNova startup
- Typically created during ideation/pitch phase
- Can have multiple versions as you iterate (`-v1`, `-v2`, etc.)

**No Suffix:**
- Used for **MVP (Minimum Viable Product) applications**
- Example: `moneynova.illinihunt.org` → Working MoneyNova app
- Represents your actual functional product
- Direct, clean URL for your live application

**Why this matters:**
- Landing pages (versioned) can change frequently without affecting your MVP URL
- MVP URL (`yourproject.illinihunt.org`) remains stable for users and testing
- Clear separation between marketing/landing content and functional app

### What If My Request Fails?

The automation will comment on your issue with the specific error. Common issues:

- **Not authorized:** Your GitHub username isn't in the allowlist
- **Invalid subdomain:** Check naming rules above
- **Invalid URL:** Must be a valid `bolt.host` URL
- **Subdomain exists:** Use `update` action instead of `new`

## For Instructors

### Initial Setup

#### 1. Create GitHub Repository

```bash
# Create repo on GitHub first, then:
cd /path/to/practicum
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

#### 2. Add Students to Allowlist

Edit `allowlist.txt` and add student GitHub usernames (one per line):

```
student-username1
student-username2
student-username3
```

Commit and push:

```bash
git add allowlist.txt
git commit -m "Update student allowlist"
git push
```

#### 3. Configure GitHub Secrets

Go to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add secret:
- **Name:** `CLOUDFLARE_API_TOKEN`
- **Value:** Your Cloudflare API token

**To get Cloudflare API Token:**
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Click **My Profile** → **API Tokens**
3. Click **Create Token**
4. Create custom token with permissions:
   - Account: `Workers Scripts:Edit`
   - Zone: `illinihunt.org` → `Workers Routes:Edit`
   - Zone: `illinihunt.org` → `DNS:Edit` (for automatic DNS record creation)
5. Copy the token and add as GitHub secret

#### 4. Test the Workflow

Create a test issue to verify everything works:
1. Add your own GitHub username to `allowlist.txt`
2. Create a subdomain request issue
3. Verify automation runs successfully

### Managing Subdomains

#### View All Subdomains

Check `subdomains.json` or run:

```bash
cat subdomains.json | jq '.subdomains'
```

#### Manual Updates

If you need to manually update subdomains:

```bash
# 1. Edit subdomains.json
nano subdomains.json

# 2. Generate worker code
python3 generate-worker.py

# 3. Deploy
wrangler deploy

# 4. Commit
git add subdomains.json cloudflare-worker.js
git commit -m "Manual update: subdomain changes"
git push
```

#### Remove a Subdomain

1. Edit `subdomains.json` and remove the entry
2. Run `python3 generate-worker.py`
3. Run `wrangler deploy`
4. Commit and push changes

### Monitoring

- **GitHub Actions logs:** See all workflow runs under **Actions** tab
- **Cloudflare logs:** Dashboard → Workers & Pages → illinihunt-reverse-proxy → Logs
- **Issue history:** All subdomain requests tracked as GitHub issues

## Technical Details

### Architecture

```
GitHub Issue (Student Request)
    ↓
GitHub Actions Workflow
    ↓
Allowlist Check → Parse Issue → Validate Input
    ↓
Update subdomains.json
    ↓
Generate cloudflare-worker.js
    ↓
Create DNS Record (via Cloudflare API)
    ↓
Deploy Worker via Wrangler
    ↓
Commit Changes → Comment on Issue (Success/Failure)
```

### Files

- **`subdomains.json`** - Configuration file mapping subdomains to bolt.host projects
- **`generate-worker.py`** - Generates Cloudflare Worker JavaScript from config
- **`cloudflare-worker.js`** - Auto-generated worker code (deployed to Cloudflare)
- **`wrangler.toml`** - Wrangler CLI configuration
- **`allowlist.txt`** - Authorized student GitHub usernames
- **`.github/workflows/process-subdomain-request.yml`** - GitHub Actions workflow
- **`.github/scripts/process-subdomain-request.py`** - Issue parser and validator
- **`.github/scripts/manage-dns.py`** - DNS record management via Cloudflare API
- **`.github/ISSUE_TEMPLATE/subdomain-request.md`** - Issue template for students

### Security Features

- **Allowlist validation:** Only authorized users can request subdomains
- **Input validation:** Subdomain names and URLs are validated
- **Concurrency control:** Prevents duplicate workflow runs
- **Auto-close on success:** Issues are automatically closed when deployed

### Workflow Permissions

The GitHub Actions workflow requires:
- `issues: write` - To comment on and close issues
- `contents: write` - To commit subdomain configuration updates

## Troubleshooting

### Student Request Failed

Check the workflow logs:
1. Go to **Actions** tab
2. Click the failed workflow run
3. Check the error message in the logs

### Deployment Not Working

Verify:
1. `CLOUDFLARE_API_TOKEN` secret is set correctly
2. Token has correct permissions
3. `wrangler.toml` has correct account ID

### Subdomain Not Accessible

1. Check subdomain was deployed: `curl https://subdomain.illinihunt.org`
2. Verify DNS records in Cloudflare Dashboard
3. Wait 2-5 minutes for DNS propagation
4. Check Cloudflare Worker logs

## Development

### Local Testing

Test the parser script:

```bash
python3 .github/scripts/process-subdomain-request.py "$(cat <<EOF
**Subdomain Name:** test-v1
**Bolt.host URL:** https://test-project-abc.bolt.host/
**Action:** new
EOF
)"
```

Test worker generation and deployment:

```bash
python3 generate-worker.py
wrangler deploy
```

### Adding New Features

1. Create a new branch
2. Make changes
3. Test thoroughly
4. Submit PR
5. Merge to main

## License

Internal use for course: BADM 350 (Course ID: badm_350_120255_247989)

## Support

For issues or questions:
- **Students:** Create an issue or contact instructor
- **Instructors:** Check GitHub Actions logs and Cloudflare dashboard
