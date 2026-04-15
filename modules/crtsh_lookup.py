import requests

def get_crtsh_data(domain):
    """
    Query crt.sh certificate transparency logs for subdomains.
    Handles SAN entries that contain newlines (multiple domains per cert).
    Filters wildcards. Returns up to 20 unique subdomains.
    """
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return []

        data = response.json()
        subdomains = set()

        for entry in data:
            # name_value can contain \n-separated SANs
            names = entry["name_value"].split("\n")
            for name in names:
                name = name.strip()
                if name and "*" not in name:
                    subdomains.add(name)

        return list(subdomains)[:20]

    except Exception as e:
        print(f"[!] crt.sh error: {e}")
        return []
