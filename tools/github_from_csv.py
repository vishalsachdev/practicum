#!/usr/bin/env python3
import argparse
import csv
import os
import re
import subprocess
import sys
from typing import Iterable, List, Set


def _clean_headers(row: dict) -> dict:
    cleaned = {}
    for k, v in row.items():
        if k is None:
            continue
        key = re.sub(r"[\s_]+", " ", k.strip().strip(",").lower())
        cleaned[key] = (v or "").strip()
    return cleaned


def extract_repos(csv_path: str) -> List[str]:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    seen: Set[str] = set()
    repos: List[str] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            row = _clean_headers(raw)
            url = (
                row.get("github url")
                or row.get("github")
                or row.get("repo url")
                or row.get("repository url")
                or row.get("repo")
                or ""
            ).strip()
            if not url:
                continue
            # Normalize OWNER/REPO from URL or raw owner/repo
            owner_repo = None
            if "://" in url:
                # URL form
                m = re.search(r"github\.com/([^/]+)/([^/#?]+)", url, re.I)
                if m:
                    owner = m.group(1)
                    repo = m.group(2).removesuffix(".git")
                    owner_repo = f"{owner}/{repo}"
            else:
                # Possibly already OWNER/REPO
                m = re.match(r"^[^/]+/[^/]+$", url)
                if m:
                    owner_repo = url
            if not owner_repo:
                continue
            if owner_repo not in seen:
                repos.append(owner_repo)
                seen.add(owner_repo)
    return repos


def run(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=False, text=True, capture_output=True)


def list_pending_invites(repos: Iterable[str]) -> List[tuple]:
    # Query all pending invites
    q = run([
        "gh",
        "api",
        "-H",
        "Accept: application/vnd.github+json",
        "/user/repository_invitations",
        "--paginate",
        "--jq",
        ".[ ] | map([.id, .repository.full_name, .inviter.login, .created_at] | @tsv) | .[]",
    ])
    if q.returncode != 0:
        print(q.stderr.strip() or q.stdout.strip(), file=sys.stderr)
        return []
    wanted = set(repos)
    out: List[tuple] = []
    for line in q.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        inv_id, full, inviter, created = parts[:4]
        if full in wanted:
            out.append((inv_id, full, inviter, created))
    return out


def accept_invites(ids: Iterable[str]) -> int:
    count = 0
    for inv_id in ids:
        if not inv_id:
            continue
        r = run(["gh", "api", "-X", "PATCH", f"/user/repository_invitations/{inv_id}"])
        if r.returncode == 0:
            count += 1
        else:
            print(f"Failed to accept {inv_id}: {r.stderr or r.stdout}", file=sys.stderr)
    return count


def report_access(repos: Iterable[str]) -> None:
    print("Repo\tVisibility\tViewerPermission")
    for r in repos:
        if not r:
            continue
        q = run([
            "gh",
            "repo",
            "view",
            r,
            "--json",
            "visibility,viewerPermission",
            "-q",
            f"\"{r}\t\" + .visibility + \"\t\" + (.viewerPermission // \"NONE\")",
        ])
        if q.returncode != 0:
            print(f"{r}\tUNKNOWN\tNO_ACCESS_OR_NOT_FOUND")
        else:
            sys.stdout.write(q.stdout)


def main():
    ap = argparse.ArgumentParser(description="Use a frozen CSV of student repos for GitHub checks.")
    ap.add_argument("csv", nargs="?", default="data/students.csv", help="Path to CSV (default: data/students.csv)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-repos", help="Print normalized OWNER/REPO lines from CSV")
    sub.add_parser("pending", help="List pending invitations among CSV repos")
    sub.add_parser("accept", help="Accept pending invitations for CSV repos")
    sub.add_parser("access", help="Show visibility and your permission for CSV repos")

    args = ap.parse_args()
    repos = extract_repos(args.csv)

    if args.cmd == "list-repos":
        print("\n".join(repos))
        return

    if args.cmd in ("pending", "accept"):
        pending = list_pending_invites(repos)
        if args.cmd == "pending":
            if not pending:
                print("No pending invitations for repos in CSV.")
                return
            print("Pending invites:")
            for inv_id, full, inviter, created in pending:
                print(f"- {full} — ID={inv_id}, inviter={inviter}, created={created}")
            return
        # accept
        if not pending:
            print("No pending invitations to accept for repos in CSV.")
            return
        accepted = accept_invites([p[0] for p in pending])
        print(f"Accepted {accepted} invitation(s).")
        return

    if args.cmd == "access":
        report_access(repos)
        return


if __name__ == "__main__":
    main()

