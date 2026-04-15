import requests
from config import GITHUB_TOKEN

def search_github_org(org_name):
    """
    Fetch public repositories for a GitHub organisation.
    Returns empty list if org does not exist or has no public repos.
    Skips lookup if org_name is too short to be meaningful (< 3 chars).
    """
    if len(org_name) < 3:
        return []

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        url = f"https://api.github.com/orgs/{org_name}/repos"
        params = {"per_page": 10, "sort": "updated"}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            repos = response.json()
            if not isinstance(repos, list):
                return []
            return [{
                "name": r["name"],
                "url": r["html_url"],
                "language": r.get("language") or "Unknown",
                "stars": r.get("stargazers_count", 0)
            } for r in repos]
        return []
    except Exception:
        return []
