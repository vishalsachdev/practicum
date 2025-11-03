#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
from typing import Dict, List, Optional, Tuple


def sh(cmd: list, input: Optional[str] = None, env: Optional[dict] = None) -> Tuple[int, str, str]:
    # If env is provided, merge with existing environment
    run_env = None
    if env:
        run_env = os.environ.copy()
        run_env.update(env)
    p = subprocess.run(cmd, input=input, text=True, capture_output=True, env=run_env)
    return p.returncode, p.stdout, p.stderr


def parse_csv(csv_path: str) -> List[dict]:
    rows: List[dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def normalize_repo(url: str) -> Optional[Tuple[str, str]]:
    if not url:
        return None
    url = url.strip()
    if not url:
        return None
    if "://" in url:
        m = re.search(r"github\.com/([^/]+)/([^/#?]+)", url, re.I)
        if not m:
            return None
        owner, repo = m.group(1), m.group(2)
    else:
        parts = url.split("/")
        if len(parts) != 2:
            return None
        owner, repo = parts
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


def iso(dt_obj: dt.datetime) -> str:
    # Convert to UTC if timezone-aware, otherwise assume UTC
    if dt_obj.tzinfo is not None:
        dt_obj = dt_obj.astimezone(dt.timezone.utc)
    # Format as ISO8601 with Z suffix
    return dt_obj.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


VERBOSE = os.getenv("LEADERBOARD_VERBOSE") == "1"


def gh_json(args: list) -> Optional[object]:
    # GitHub CLI automatically uses GH_TOKEN or GITHUB_TOKEN from environment
    # Just pass the environment through
    code, out, err = sh(["gh", "api", *args])
    if code != 0:
        if VERBOSE and err:
            print(f"Warning: GitHub API call failed: {err}", file=sys.stderr)
        return None
    try:
        return json.loads(out)
    except Exception as e:
        if VERBOSE:
            print(f"Warning: Failed to parse JSON: {e}", file=sys.stderr)
        return None


def commits_since(owner: str, repo: str, since_iso: str, author: Optional[str]) -> List[dict]:
    # Build query string for GitHub API
    query_params = f"since={since_iso}&per_page=100"
    if author:
        query_params += f"&author={author}"
    args = [f"/repos/{owner}/{repo}/commits?{query_params}"]
    data = gh_json(args)
    if not isinstance(data, list):
        return []
    return data


def search_total(q: str) -> int:
    data = gh_json(["/search/issues", "-F", f"q={q}"])
    if not isinstance(data, dict):
        return 0
    return int(data.get("total_count", 0))


def has_repo_access(owner: str, repo: str) -> bool:
    """Return True if the current token can view the repo (public or collaborator)."""
    code, out, err = sh([
        "gh",
        "repo",
        "view",
        f"{owner}/{repo}",
        "--json",
        "name",
        "-q",
        ".name",
    ])
    return code == 0 and (out.strip() != "")


def load_subdomains(subdomains_path: str = "subdomains.json") -> Dict[str, str]:
    """Load subdomain mappings from JSON file"""
    try:
        with open(subdomains_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("subdomains", {})
    except Exception:
        return {}


def extract_bolt_project_id(app_url: str) -> Optional[str]:
    """Extract bolt.host project ID from URL"""
    if not app_url:
        return None
    app_url = app_url.strip().rstrip("/")
    # Match patterns like https://project-id.bolt.host or project-id.bolt.host
    import re
    match = re.search(r"([a-z0-9-]+)\.bolt\.host", app_url, re.I)
    if match:
        return match.group(1)
    return None


def find_subdomain_for_bolt_id(bolt_id: str, subdomains: Dict[str, str]) -> Optional[str]:
    """Find subdomain name that maps to this bolt project ID"""
    for subdomain, mapped_id in subdomains.items():
        # Handle both project IDs and full URLs
        if mapped_id == bolt_id:
            return subdomain
        # Also check if mapped_id contains the bolt_id (for full URLs)
        if bolt_id in mapped_id:
            return subdomain
    return None


def build_from_csv(csv_path: str, days_window: int = 7, subdomains_path: str = "subdomains.json") -> Dict:
    rows = parse_csv(csv_path)
    subdomains = load_subdomains(subdomains_path)
    now = dt.datetime.now(dt.timezone.utc)
    since7 = now - dt.timedelta(days=days_window)
    since30 = now - dt.timedelta(days=30)

    students: List[Dict] = []
    skipped: List[Dict] = []
    for r in rows:
        name = (r.get("Name") or r.get("name") or "").strip()
        url = (r.get("Github URL") or r.get("github url") or r.get("github") or "").strip()
        if not url:
            continue
        nr = normalize_repo(url)
        if not nr:
            continue
        owner, repo = nr
        # Skip quietly if no access (private or missing)
        if not has_repo_access(owner, repo):
            skipped.append({"name": name or owner, "repo": f"{owner}/{repo}", "reason": "no_access_or_missing"})
            continue
        author = owner  # assume repo owner is the student

        # Commits - don't filter by author as some commits may not have GitHub login
        # This ensures we capture all commits, including those from org repos or commits without login
        commits7 = commits_since(owner, repo, iso(since7), author=None)
        commits30 = commits_since(owner, repo, iso(since30), author=None)

        # Unique commit days for last 7
        days7 = set()
        for c in commits7:
            try:
                d = c["commit"]["author"]["date"][:10]
                days7.add(d)
            except Exception:
                pass

        # PRs opened and merged in last 7
        # Note: We still filter PRs by author since PRs typically have GitHub logins
        since_date = since7.date().isoformat()
        q_opened = f"repo:{owner}/{repo} is:pr author:{author} created:>={since_date}"
        q_merged = f"repo:{owner}/{repo} is:pr author:{author} is:merged merged:>={since_date}"
        pr_opened_7d = search_total(q_opened)
        pr_merged_7d = search_total(q_merged)

        # Streak (based on last 30 days commit dates)
        dayset = set()
        for c in commits30:
            try:
                d = c["commit"]["author"]["date"][:10]
                dayset.add(d)
            except Exception:
                pass
        streak = 0
        cur = now.date()
        while True:
            key = cur.isoformat()
            if key in dayset:
                streak += 1
                cur = cur - dt.timedelta(days=1)
            else:
                break

        # Score
        commits_7d = len(commits7)
        commit_days_7d = len(days7)
        score = (
            commits_7d * 1
            + commit_days_7d * 2
            + pr_opened_7d * 3
            + pr_merged_7d * 5
        )

        # Badges
        badges = []
        if streak >= 7:
            badges.append("week-warrior")
        if pr_opened_7d >= 1:
            badges.append("pr-starter")
        if pr_merged_7d >= 1:
            badges.append("merge-master")
        if commits_7d >= 5:
            badges.append("commit-cadence")

        # Get App URL and find subdomain
        app_url = (r.get("App URL") or r.get("app url") or "").strip()
        bolt_id = extract_bolt_project_id(app_url)
        subdomain_name = None
        illinihunt_url = None
        
        if bolt_id:
            # Find subdomain that maps to this bolt project ID
            subdomain_name = find_subdomain_for_bolt_id(bolt_id, subdomains)
            if subdomain_name:
                illinihunt_url = f"https://{subdomain_name}.illinihunt.org"
        
        # Normalize bolt URL
        bolt_url = None
        if app_url:
            app_url = app_url.strip().rstrip("/")
            if "bolt.host" in app_url:
                if not app_url.startswith("http"):
                    bolt_url = f"https://{app_url}"
                else:
                    bolt_url = app_url
            elif app_url.startswith("http"):
                # Full URL (e.g., Vercel)
                bolt_url = app_url

        students.append(
            {
                "name": name or owner,
                "repo": f"{owner}/{repo}",
                "owner": owner,
                "metrics": {
                    "commits_7d": commits_7d,
                    "commit_days_7d": commit_days_7d,
                    "commits_30d": len(commits30),
                    "pr_opened_7d": pr_opened_7d,
                    "pr_merged_7d": pr_merged_7d,
                    "streak": streak,
                    "score": score,
                },
                "badges": badges,
                "urls": {
                    "bolt": bolt_url,
                    "illinihunt": illinihunt_url,
                },
            }
        )

    # Leaderboard
    students.sort(key=lambda s: (-s["metrics"]["score"], -s["metrics"]["streak"], s["name"].lower()))
    leaderboard = []
    rank = 0
    last_score = None
    for s in students:
        sc = s["metrics"]["score"]
        if sc != last_score:
            rank = len(leaderboard) + 1
            last_score = sc
        leaderboard.append({"name": s["name"], "repo": s["repo"], "score": sc, "rank": rank})

    return {
        "generated_at": iso(now),
        "window_days": days_window,
        "students": students,
        "leaderboard": leaderboard,
        "skipped": skipped,
    }


def main():
    ap = argparse.ArgumentParser(description="Build a static leaderboard JSON from a frozen CSV.")
    ap.add_argument("csv", help="Path to CSV, e.g. data/students.csv")
    ap.add_argument("out", help="Output JSON path, e.g. web/leaderboard.json")
    ap.add_argument("--days", type=int, default=7, help="Window in days (default 7)")
    ap.add_argument("--subdomains", default="subdomains.json", help="Path to subdomains.json (default: subdomains.json)")
    args = ap.parse_args()

    data = build_from_csv(args.csv, days_window=args.days, subdomains_path=args.subdomains)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
