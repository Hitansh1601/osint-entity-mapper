import shodan
from config import SHODAN_API_KEY

def get_shodan_data(ip):
    """
    Look up an IP on Shodan for open ports, OS, org, and known vulnerabilities.
    Handles both API errors (quota, not found) and network errors gracefully.
    """
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        host = api.host(ip)
        return {
            "org": host.get("org", "Unknown"),
            "os": host.get("os") or "Unknown",  # os can be None not missing
            "ports": host.get("ports", []),
            "country": host.get("country_name", "Unknown"),
            "vulns": list(host.get("vulns", []))
        }
    except shodan.APIError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
