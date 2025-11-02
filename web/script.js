// Load and display leaderboard data
async function loadLeaderboard() {
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');
    const containerEl = document.getElementById('leaderboard-container');
    const contentEl = document.getElementById('leaderboard-content');

    try {
        const response = await fetch('leaderboard.json');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        loadingEl.style.display = 'none';

        // Update meta information
        if (data.generated_at) {
            const date = new Date(data.generated_at);
            document.getElementById('generated-at').textContent = 
                `Updated ${date.toLocaleString()}`;
        }
        if (data.window_days) {
            document.getElementById('window-days').textContent = data.window_days;
        }

        // Calculate summary statistics
        const totalCommits = data.students.reduce((sum, s) => sum + s.metrics.commits_7d, 0);
        const totalPRs = data.students.reduce((sum, s) => sum + s.metrics.pr_merged_7d, 0);

        document.getElementById('total-students').textContent = data.students.length;
        document.getElementById('total-commits').textContent = totalCommits;
        document.getElementById('total-prs').textContent = totalPRs;

        // Render leaderboard
        renderLeaderboard(data.students, 'comprehensive');
        containerEl.style.display = 'block';

        // Set up view toggle
        document.getElementById('view-comprehensive').addEventListener('click', () => {
            document.getElementById('view-comprehensive').classList.add('active');
            document.getElementById('view-simple').classList.remove('active');
            renderLeaderboard(data.students, 'comprehensive');
        });

        document.getElementById('view-simple').addEventListener('click', () => {
            document.getElementById('view-simple').classList.add('active');
            document.getElementById('view-comprehensive').classList.remove('active');
            renderLeaderboard(data.students, 'simple');
        });

    } catch (error) {
        console.error('Error loading leaderboard:', error);
        loadingEl.style.display = 'none';
        errorEl.style.display = 'block';
    }
}

function renderLeaderboard(students, viewMode) {
    const contentEl = document.getElementById('leaderboard-content');
    contentEl.innerHTML = '';

    students.forEach((student, index) => {
        const item = document.createElement('div');
        item.className = `leaderboard-item ${viewMode}`;

        const rank = student.metrics.score > 0 ? index + 1 : '-';
        const rankClass = rank === 1 ? 'rank-1' : rank === 2 ? 'rank-2' : rank === 3 ? 'rank-3' : '';

        // Determine primary identifier - use illinihunt domain if available, otherwise repo name
        const primaryIdentifier = student.urls && student.urls.illinihunt 
            ? student.urls.illinihunt.replace('https://', '') 
            : student.repo;
        
        const primaryLink = student.urls && student.urls.illinihunt
            ? student.urls.illinihunt
            : `https://github.com/${student.repo}`;

        let html = `
            <div class="rank ${rankClass}">${rank === '-' ? '—' : rank}</div>
            <div class="student-info">
                <div class="student-domain">
                    <a href="${escapeHtml(primaryLink)}" target="_blank" rel="noopener noreferrer" class="primary-domain-link">
                        ${escapeHtml(primaryIdentifier)}
                    </a>
                </div>
                <div class="student-repo">
                    <span>📦</span>
                    <a href="https://github.com/${student.repo}" target="_blank" rel="noopener noreferrer">
                        ${escapeHtml(student.repo)}
                    </a>
                </div>
        `;

        // Add URLs (bolt.host only - illinihunt is already shown as primary identifier)
        if (student.urls && student.urls.bolt) {
            html += '<div class="student-urls">';
            html += `<a href="${escapeHtml(student.urls.bolt)}" target="_blank" rel="noopener noreferrer" class="url-link bolt-link">
                🔗 ${escapeHtml(student.urls.bolt.replace('https://', '').replace('http://', ''))}
            </a>`;
            html += '</div>';
        }

        if (viewMode === 'comprehensive') {
            // Badges
            if (student.badges && student.badges.length > 0) {
                html += '<div class="badges">';
                student.badges.forEach(badge => {
                    const badgeLabels = {
                        'week-warrior': '🔥 Week Warrior',
                        'pr-starter': '🚀 PR Starter',
                        'merge-master': '✨ Merge Master',
                        'commit-cadence': '⚡ Commit Cadence'
                    };
                    html += `<span class="badge ${badge}">${badgeLabels[badge] || badge}</span>`;
                });
                html += '</div>';
            }

            // Metrics
            html += '<div class="metrics">';
            html += `<div class="metric">
                <div class="metric-label">Commits (7d)</div>
                <div class="metric-value">${student.metrics.commits_7d}</div>
            </div>`;
            html += `<div class="metric">
                <div class="metric-label">Commit Days</div>
                <div class="metric-value">${student.metrics.commit_days_7d}</div>
            </div>`;
            html += `<div class="metric">
                <div class="metric-label">PRs Opened</div>
                <div class="metric-value">${student.metrics.pr_opened_7d}</div>
            </div>`;
            html += `<div class="metric">
                <div class="metric-label">PRs Merged</div>
                <div class="metric-value">${student.metrics.pr_merged_7d}</div>
            </div>`;
            html += `<div class="metric">
                <div class="metric-label">
                    Streak
                    <span class="info-icon" title="Consecutive days with commits, counting backwards from today">ℹ️</span>
                </div>
                <div class="metric-value">${student.metrics.streak} 🔥</div>
            </div>`;
            html += '</div>';
        }

        html += '</div>';
        html += `<div class="score">
            <div class="score-value">${student.metrics.score}</div>
            <div class="score-label">Score</div>
        </div>`;
        html += '</div>';

        item.innerHTML = html;
        contentEl.appendChild(item);
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load leaderboard on page load
document.addEventListener('DOMContentLoaded', loadLeaderboard);

