import os
import requests
import subprocess


GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
BASE_URL = "https://api.github.com"

def fetch_stalled_prs(owner, repo):
    """Fetch stalled PRs with the `stalled` label"""
    url = f"{BASE_URL}"/search/issues
    query = f"repo:{owner}/{repo} label:stalled is:pr is:open"
    response = requests.get(url, headers=HEADERS, params={"q": query})
    response.raise_for_status()
    return response.json()["items"]

def rebase_pr(repo_dir, pr_branch, target_branch):
    """Rebase a stalled PR onto the target branch."""
    subprocess.run(["git","checkout",pr_branch], cwd=repo_dir)
    subprocess.run(["git","fetch","origin", target_branch], cwd=repo_dir)
    subprocess.run(["git","rebase",f"origin"/{target_branch}], cwd=repo_dir)
    subprocess.run(["git","push","--force-with-lease"], cwd=repo_dir)

def main_stalled(owner, repo, repo_dir):
    """Main function to handle stalled PRs"""
    stalled_prs = fetch_stalled_prs(owner,repo)
    for pr in stalled_prs:
        pr_number = pr["number"]
        pr_details = fetch_stalled_prs(owner, repo, pr_number)
        pr_branch = pr_details["head"]["ref"]
        target_branch = pr_details["base"]["ref"]
        print(f"Handling Stalled PR #{pr_number}: {pr_branch} -> {target_branch}")
        rebase_pr(repo_dir, pr_branch, target_branch)


