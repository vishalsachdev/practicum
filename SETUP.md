# Quick Setup Guide

Follow these steps to set up the automated subdomain management system.

## Prerequisites

- ✅ Cloudflare account with Workers access
- ✅ Domain (illinihunt.org) configured in Cloudflare
- ✅ Cloudflare Worker already deployed (illinihunt-reverse-proxy)
- ✅ GitHub account

## Step-by-Step Setup

### 1. Create GitHub Repository

```bash
# On GitHub.com:
# 1. Go to https://github.com/new
# 2. Create new repository (e.g., "illinihunt-subdomains")
# 3. Make it Private
# 4. Don't initialize with README (we already have files)

# Then locally:
cd /Users/vishal/Desktop/practicum
git remote add origin https://github.com/YOUR-USERNAME/illinihunt-subdomains.git
git branch -M main
git push -u origin main
```

### 2. Get Cloudflare API Token

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click **Create Token**
3. Create custom token with permissions:
   - Account: `Workers Scripts:Edit`
   - Zone: `illinihunt.org` → `Workers Routes:Edit`
   - Zone: `illinihunt.org` → `DNS:Edit` (for automatic DNS record creation)
4. Click **Continue to Summary** → **Create Token**
5. **Copy the token** (you'll only see it once!)

**Note:** The token needs DNS edit permissions to automatically create DNS records for new subdomains.

### 3. Add GitHub Secret

1. Go to your GitHub repo
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `CLOUDFLARE_API_TOKEN`
5. Value: Paste the token from step 2
6. Click **Add secret**

### 4. Add Student Usernames to Allowlist

Edit `allowlist.txt`:

```bash
nano allowlist.txt
```

Add student GitHub usernames (one per line):

```
student1-github-username
student2-github-username
student3-github-username
```

**To get student GitHub usernames:**
- Ask students to provide their GitHub username
- Or look them up on GitHub
- Format: just the username, no @ symbol

Save and commit:

```bash
git add allowlist.txt
git commit -m "Add student allowlist"
git push
```

### 5. Test the Automation

Create a test issue to verify everything works:

1. Add your own GitHub username to `allowlist.txt`
2. Go to GitHub repo → **Issues** → **New Issue**
3. Select **Subdomain Request** template
4. Fill in:
   ```
   Subdomain Name: test-subdomain
   Bolt.host URL: https://some-working-bolt-site.bolt.host/
   Action: new
   ```
5. Click **Submit new issue**
6. Watch the **Actions** tab - workflow should start automatically
7. Within 1-2 minutes, you should see a success comment
8. Test the subdomain: `https://test-subdomain.illinihunt.org`

### 6. Share Instructions with Students

Send students:
1. Link to your GitHub repo
2. Instructions to create subdomain request issues
3. Their GitHub username must be in allowlist

**Student Instructions Template:**

```
To get a subdomain for your project:

1. Create your site on bolt.host and copy the URL
2. Go to: [YOUR GITHUB REPO URL]/issues/new/choose
3. Select "Subdomain Request"
4. Fill in your subdomain name and bolt.host URL
5. Submit the issue
6. Wait 1-2 minutes for the automation to process it
7. Your subdomain will be: https://[your-subdomain].illinihunt.org

Make sure your GitHub username is in the allowlist first!
```

## Verification Checklist

- [ ] GitHub repo created and code pushed
- [ ] `CLOUDFLARE_API_TOKEN` secret added to GitHub
- [ ] Student usernames added to `allowlist.txt`
- [ ] Test issue created and processed successfully
- [ ] Test subdomain is accessible
- [ ] Students have been notified

## Troubleshooting

### Workflow Not Running

- Check that issue has `subdomain-request` label (auto-applied by template)
- Verify workflow file exists: `.github/workflows/process-subdomain-request.yml`
- Check **Actions** tab is enabled for the repo

### "Not Authorized" Error

- Verify student's exact GitHub username is in `allowlist.txt`
- No extra spaces or @ symbols
- Case-sensitive match
- Re-push `allowlist.txt` after changes

### Deployment Failed

- Check `CLOUDFLARE_API_TOKEN` is set correctly
- Verify token has Workers edit permissions
- Check `wrangler.toml` has correct account_id
- View detailed error in Actions logs

### Subdomain Not Working

- Wait 2-5 minutes for DNS propagation
- Check if DNS record exists in Cloudflare dashboard
- Verify bolt.host URL works directly
- Check Cloudflare Worker logs

## Next Steps

Once setup is complete:

1. **Monitor issues** - Students will create subdomain requests
2. **Check Actions logs** - Review workflow runs for errors
3. **Update allowlist** - Add/remove students as needed
4. **Manual overrides** - Use `wrangler deploy` if needed

## Support

For technical issues:
- Check GitHub Actions logs
- Review Cloudflare Worker logs
- See README.md for detailed troubleshooting
