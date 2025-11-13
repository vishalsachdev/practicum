# Illinihunt.org — Student Startup Infrastructure

**Automated subdomain management and GitHub activity leaderboard for BADM 372 student startups.**

This system provides the infrastructure for [BADM 372 – Information Systems & Operations Management Practicum](https://practicum.web.illinois.edu/syllabus/), where students become solo-preneurs, building and deploying entire startups independently in 15 weeks using AI coding tools (Lovable, Bolt, Cursor, Windsurf) as their technical co-pilots.

## 🎯 What This System Does

1. **Automated Subdomain Management** — Students request `*.illinihunt.org` subdomains via GitHub issues, and the system automatically validates, configures DNS, and deploys their projects
2. **GitHub Activity Leaderboard** — Tracks and visualizes student engagement through commits, PRs, streaks, and badges
3. **Multi-Platform Support** — Works with bolt.host, Vercel, Netlify, Render, Fly.io, and other hosting platforms
4. **Self-Service Workflow** — Students submit issues to request or update subdomains without instructor intervention

## 📚 Documentation

- **[README.md](README.md)** (this file) — Overview and getting started guide
- **[SETUP.md](SETUP.md)** — Step-by-step setup instructions for instructors
- **[DEPLOY.md](DEPLOY.md)** — Quick deployment guide for subdomain updates
- **[CLAUDE.md](CLAUDE.md)** — Technical documentation and common commands
- **[MVP_EVALUATION_REPORT.md](MVP_EVALUATION_REPORT.md)** — Evaluation of 15 student MVP applications
- **[SUBDOMAINS.md](SUBDOMAINS.md)** — Current subdomain mappings and details
- **[web/README.md](web/README.md)** — Leaderboard frontend documentation

## 🏆 Live Leaderboard

View the live GitHub activity leaderboard at: **https://vishalsachdev.github.io/practicum/**

The leaderboard tracks:
- **Commits** (7-day window)
- **Commit Days** (unique days with activity)
- **Pull Requests** (opened and merged)
- **Streaks** (consecutive days with commits)
- **Badges** (achievements and milestones)
- **MVP Links** (deployed applications on illinihunt.org)

The leaderboard updates automatically daily at 6 AM UTC and can be manually triggered via GitHub Actions.

## 👨‍🎓 For Students

### How to Request a Subdomain

1. **Create your project** on bolt.host, Vercel, Netlify, or another supported platform and note the URL (e.g., `https://my-project-abc123.bolt.host/`)

2. **Create a GitHub Issue** using the "Subdomain Request" template:
   - Click **Issues** → **New Issue**
   - Select **Subdomain Request** template
   - Fill in:
     - **Subdomain Name:** Your desired subdomain (e.g., `myproject-v1`)
     - **Platform URL:** Your full project URL (bolt.host, Vercel, Netlify, etc.)
     - **Action:** `new` (for first-time) or `update` (to change URL) — *optional, auto-detected if omitted*
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
- Used for **teaser campaign landing pages** at the **pre-launch phase**
- Example: `moneynova-v1.illinihunt.org` → Pre-launch teaser for MoneyNova
- Purpose: Build awareness, collect early signups, gauge interest before MVP launch
- Can have multiple versions as you test different messaging (`-v1`, `-v2`, etc.)
- Temporary URLs for marketing campaigns

**No Suffix:**
- Used for **MVP (Minimum Viable Product) applications**
- Example: `moneynova.illinihunt.org` → Live MoneyNova app
- Represents your actual functional product
- Direct, clean URL for your live application
- This is your permanent production URL

**Typical Student Workflow:**
1. **Pre-launch Phase:** Deploy teaser landing page at `project-v1.illinihunt.org`
2. **Test & Iterate:** Update messaging with `project-v2.illinihunt.org`
3. **Launch Phase:** Deploy MVP app at `project.illinihunt.org`
4. **Post-launch:** MVP URL becomes canonical, teaser pages archived

**Why this matters:**
- Teaser campaigns (versioned) won't interfere with your MVP launch
- MVP URL (`yourproject.illinihunt.org`) remains stable for users and investors
- Clear separation between pre-launch marketing and functional product
- Professional, clean URL for your production application

### Supported Platforms

The system supports multiple hosting platforms:

- **bolt.host** — `https://project-id.bolt.host` or `https://project-id.bolt.new`
- **Vercel** — `https://project-name.vercel.app`
- **Netlify** — `https://project-name.netlify.app`
- **Render** — `https://project-name.onrender.com`
- **Fly.io** — `https://project-name.fly.dev`

For bolt.host, only the project ID is stored (e.g., `project-abc123`). For other platforms, the full URL is stored.

### What If My Request Fails?

The automation will comment on your issue with the specific error. Common issues:

- **Not authorized:** Your GitHub username isn't in the allowlist
- **Invalid subdomain:** Check naming rules above
- **Invalid URL:** Must be a valid URL from a supported platform
- **Subdomain exists:** Use `update` action instead of `new` (or omit the action field for auto-detection)

### Reporting Issues

If you notice problems with the leaderboard or your subdomain:

- **[Leaderboard Issue](https://github.com/vishalsachdev/practicum/issues/new?template=leaderboard-issue.md)** — Report incorrect data, missing repos, or URL problems
- **[Subdomain Request](https://github.com/vishalsachdev/practicum/issues/new?template=subdomain-request.md)** — Request or update an illinihunt.org subdomain

## 👨‍🏫 For Instructors

### Initial Setup

See **[SETUP.md](SETUP.md)** for detailed step-by-step instructions.

**Quick Overview:**

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

**Required Secrets:**

1. **`CLOUDFLARE_API_TOKEN`** — For subdomain deployment
   - Permissions: Workers Scripts:Edit, Workers Routes:Edit, DNS:Edit

2. **`LEADERBOARD_GITHUB_TOKEN`** (optional, for private repos)
   - Personal Access Token (PAT) with `repo` scope
   - Only needed if student repositories are private
   - Falls back to `github.token` if not provided

**To get Cloudflare API Token:**
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → **My Profile** → **API Tokens**
2. Click **Create Token** → Create custom token with permissions:
   - Account: `Workers Scripts:Edit`
   - Zone: `illinihunt.org` → `Workers Routes:Edit`
   - Zone: `illinihunt.org` → `DNS:Edit` (for automatic DNS record creation)
3. Copy the token and add as GitHub secret

#### 4. Configure Leaderboard Data

Edit `data/students.csv` with student information:

```csv
Name,App URL,Github URL
"Student Name",https://project.bolt.host,https://github.com/username/repo
```

The leaderboard will automatically build and deploy daily at 6 AM UTC.

#### 5. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The leaderboard will be available at `https://[username].github.io/practicum/`

#### 6. Add Students to Allowlist

#### 6. Add Students to Allowlist

Edit `allowlist.txt` and add student GitHub usernames (one per line):

```
student-username1
student-username2
student-username3
```

Commit and push:

```bash
git add allowlist.txt data/students.csv
git commit -m "Update student data and allowlist"
git push
```

#### 7. Test the Workflow

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

See **[DEPLOY.md](DEPLOY.md)** for quick deployment instructions.

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
4. (Optional) Delete DNS record: `.github/scripts/manage-dns.py delete <subdomain>`
5. Commit and push changes

#### Bulk Operations

For bulk subdomain setup, use the bulk-setup script:

```bash
# Format: URL    subdomain@illinihunt.org (one per line)
.github/scripts/bulk-setup.py "$(cat <<'EOF'
https://project1.bolt.host    project1@illinihunt.org
https://project2.vercel.app   project2@illinihunt.org
EOF
)"
```

For bulk DNS record creation:

```bash
# Edit the script with your list of subdomains
.github/scripts/create-dns-bulk.sh
```

### Monitoring

- **GitHub Actions logs:** See all workflow runs under **Actions** tab
- **Cloudflare logs:** Dashboard → Workers & Pages → illinihunt-reverse-proxy → Logs
- **Issue history:** All subdomain requests tracked as GitHub issues
- **Leaderboard:** View student activity metrics at the live leaderboard URL
- **Test scripts:** Run `./test-subdomains.sh` to test all subdomains or `./test-urls.sh` to test source URLs

## 🔧 Technical Details

### Architecture

**Subdomain Management Flow:**

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

**Leaderboard Flow:**

```
Daily Cron Trigger (6 AM UTC) or Manual Trigger
    ↓
Read data/students.csv
    ↓
Fetch GitHub Activity (commits, PRs, streaks)
    ↓
Calculate scores and badges
    ↓
Merge with subdomains.json (MVP links)
    ↓
Generate web/leaderboard.json
    ↓
Deploy to GitHub Pages
```

### Key Files

### Key Files

**Configuration:**
- **`subdomains.json`** — Subdomain to URL mappings (source of truth)
- **`allowlist.txt`** — Authorized student GitHub usernames
- **`wrangler.toml`** — Wrangler CLI configuration
- **`data/students.csv`** — Student names, GitHub URLs, and app URLs

**Generated:**
- **`cloudflare-worker.js`** — Auto-generated worker code (don't edit manually)
- **`web/leaderboard.json`** — Auto-generated leaderboard data

**Scripts:**
- **`generate-worker.py`** — Generates Cloudflare Worker JavaScript from config
- **`tools/build_leaderboard.py`** — Builds leaderboard JSON from student data
- **`.github/scripts/process-subdomain-request.py`** — Issue parser and validator
- **`.github/scripts/manage-dns.py`** — DNS record management via Cloudflare API
- **`.github/scripts/bulk-setup.py`** — Bulk subdomain configuration
- **`test-subdomains.sh`** — Tests all configured subdomains
- **`test-urls.sh`** — Tests all source URLs

**Workflows:**
- **`.github/workflows/process-subdomain-request.yml`** — Subdomain automation workflow
- **`.github/workflows/deploy-leaderboard.yml`** — Leaderboard build and deployment

**Issue Templates:**
- **`.github/ISSUE_TEMPLATE/subdomain-request.md`** — Subdomain request template
- **`.github/ISSUE_TEMPLATE/leaderboard-issue.md`** — Leaderboard issue reporting template

**Frontend:**
- **`web/index.html`** — Leaderboard frontend HTML
- **`web/style.css`** — Leaderboard styling
- **`web/script.js`** — Leaderboard data loading and rendering

### Security Features

- **Allowlist validation:** Only authorized users can request subdomains
- **Input validation:** Subdomain names and URLs are validated
- **Concurrency control:** Prevents duplicate workflow runs
- **Auto-close on success:** Issues are automatically closed when deployed

### Workflow Permissions

**Subdomain Request Workflow:**
- `issues: write` — To comment on and close issues
- `contents: write` — To commit subdomain configuration updates

**Leaderboard Workflow:**
- `contents: read` — To read student data and configuration
- `pages: write` — To deploy to GitHub Pages
- `id-token: write` — For GitHub Pages deployment authentication

## 🔍 Troubleshooting

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
2. Verify DNS records in Cloudflare Dashboard or run: `.github/scripts/manage-dns.py list`
3. Wait 2-5 minutes for DNS propagation
4. Check Cloudflare Worker logs
5. Test with `./test-subdomains.sh` to check all subdomains

### Leaderboard Issues

**Leaderboard not updating:**
- Check workflow runs in **Actions** tab
- Verify `data/students.csv` has correct GitHub URLs
- Ensure `LEADERBOARD_GITHUB_TOKEN` secret is set (if repos are private)
- Manually trigger workflow: **Actions** → **Deploy Leaderboard to GitHub Pages** → **Run workflow**

**Missing or incorrect data:**
- Verify student GitHub URLs in `data/students.csv`
- Check that repositories are accessible (public or token has access)
- Report issues using the [Leaderboard Issue template](https://github.com/vishalsachdev/practicum/issues/new?template=leaderboard-issue.md)

## 🛠️ Development

### Local Testing

**Test subdomain request parser:**

```bash
python3 .github/scripts/process-subdomain-request.py "$(cat <<EOF
**Subdomain Name:** test-v1
**Bolt.host URL:** https://test-project-abc.bolt.host/
**Action:** new
EOF
)"
```

**Test worker generation and deployment:**

```bash
python3 generate-worker.py
wrangler deploy
```

**Test all configured subdomains:**

```bash
./test-subdomains.sh
```

**Test all source URLs:**

```bash
./test-urls.sh
```

**Build leaderboard locally:**

```bash
python3 tools/build_leaderboard.py data/students.csv web/leaderboard.json --days 7 --subdomains subdomains.json

# Then serve locally:
cd web
python3 -m http.server 8000
# Visit http://localhost:8000
```

### DNS Management

```bash
# Export Cloudflare API token
export CLOUDFLARE_API_TOKEN="your-token-here"

# Create DNS record
.github/scripts/manage-dns.py create <subdomain-name>

# List all DNS records
.github/scripts/manage-dns.py list

# Delete DNS record
.github/scripts/manage-dns.py delete <subdomain-name>
```

### Adding New Features

1. Create a new branch
2. Make changes
3. Test thoroughly
4. Submit PR
5. Merge to main

## 📊 Statistics

**Current System Stats:**
- **44+ Student Subdomains** configured and deployed
- **15 MVP Applications** evaluated ([see evaluation report](MVP_EVALUATION_REPORT.md))
- **Multi-Platform Support** — bolt.host, Vercel, Netlify, Render, Fly.io
- **Automated DNS Management** via Cloudflare API
- **Daily Leaderboard Updates** at 6 AM UTC
- **Self-Service Workflow** with issue-driven automation

## 📝 License

Internal use for course: BADM 350 (Course ID: badm_350_120255_247989)

## 🤝 Support

For issues or questions:
- **Students:** 
  - Create a [Subdomain Request](https://github.com/vishalsachdev/practicum/issues/new?template=subdomain-request.md) for subdomain issues
  - Create a [Leaderboard Issue](https://github.com/vishalsachdev/practicum/issues/new?template=leaderboard-issue.md) for leaderboard problems
  - Contact instructor for other issues
- **Instructors:** Check GitHub Actions logs, Cloudflare dashboard, and [CLAUDE.md](CLAUDE.md) for technical details

## 🔗 Quick Links

- **Live Leaderboard:** https://vishalsachdev.github.io/practicum/
- **Course Website:** https://practicum.web.illinois.edu/syllabus/
- **Cloudflare Dashboard:** https://dash.cloudflare.com
- **GitHub Actions:** [View Workflows](../../actions)
- **Issue Templates:**
  - [Subdomain Request](https://github.com/vishalsachdev/practicum/issues/new?template=subdomain-request.md)
  - [Leaderboard Issue](https://github.com/vishalsachdev/practicum/issues/new?template=leaderboard-issue.md)
