# Leaderboard Frontend

A modern, responsive web interface for displaying GitHub activity leaderboard data.

## Usage

### Local Development

1. **Generate the leaderboard JSON data:**
   ```bash
   python3 ../tools/build_leaderboard.py ../data/students.csv leaderboard.json --days 7
   ```

2. **Open the HTML file in a browser:**
   ```bash
   open index.html
   # Or serve it with a local server:
   python3 -m http.server 8000
   # Then visit http://localhost:8000
   ```

### GitHub Pages Deployment

The leaderboard is automatically deployed to GitHub Pages via GitHub Actions.

**Setup (one-time):**
1. Go to repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The workflow (`.github/workflows/deploy-leaderboard.yml`) will automatically:
   - Build the leaderboard JSON from student data
   - Deploy the frontend to GitHub Pages
   - Run daily at 6 AM UTC to keep data fresh

**Manual trigger:**
- Go to **Actions** tab → **Deploy Leaderboard to GitHub Pages** → **Run workflow**

**Live URL:**
Once enabled, the leaderboard will be available at:
`https://[username].github.io/practicum/`

Or if using a custom domain:
`https://[your-custom-domain]/`

## Features

- **Comprehensive View**: Shows full metrics (commits, PRs, streaks, badges)
- **Simple View**: Clean, minimal display with just rankings and scores
- **Real-time Stats**: Summary cards showing total students, commits, and PRs
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Badge System**: Visual indicators for achievements
- **GitHub Links**: Direct links to student repositories

## Files

- `index.html` - Main HTML structure
- `style.css` - Styling and layout
- `script.js` - Data loading and rendering logic
- `leaderboard.json` - Generated data file (created by build script)

