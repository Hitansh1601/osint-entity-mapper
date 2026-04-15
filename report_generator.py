from datetime import datetime

def generate_report(data):
    """
    Generate a structured markdown intelligence report from collected OSINT data.
    Safe against missing or empty source keys.
    Returns the filename of the saved report.
    """
    target = data["target"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Sanitise target for use in filename (remove slashes, colons etc.)
    safe_target = target.replace("/", "_").replace(":", "_")
    filename = f"report_{safe_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    sources = data.get("sources", {})
    whois  = sources.get("whois", {})
    dns    = sources.get("dns", {})
    certs  = sources.get("crtsh", [])
    github = sources.get("github", [])

    # Collect all Shodan results
    shodan_results = {
        k: v for k, v in sources.items() if k.startswith("shodan_")
    }

    lines = [
        "# OSINT Intelligence Report",
        f"**Target:** `{target}`  ",
        f"**Generated:** {timestamp}  ",
        f"**Analyst:** Hitansh Waghela  ",
        f"**Confidence:** Medium-High (5 automated sources)",
        "",
        "---",
        "",
        "## Executive Summary",
        (
            f"Automated OSINT investigation of `{target}` aggregating data from "
            "WHOIS registration records, DNS enumeration, SSL certificate transparency "
            "logs (crt.sh), Shodan infrastructure scanning, and GitHub repository discovery."
        ),
        "",
        "---",
        "",
        "## 1. WHOIS Registration Data",
        f"- **Registrar:** {whois.get('registrar', 'N/A')}",
        f"- **Organization:** {whois.get('org', 'N/A')}",
        f"- **Country:** {whois.get('country', 'N/A')}",
        f"- **Created:** {whois.get('creation_date', 'N/A')}",
        f"- **Contact Emails:** {', '.join(whois.get('emails', [])) or 'None found'}",
        "",
        "## 2. DNS Records",
        f"- **A Records (IPs):** {', '.join(dns.get('A', [])) or 'None'}",
        f"- **MX Records:** {', '.join(dns.get('MX', [])) or 'None'}",
        f"- **NS Records:** {', '.join(dns.get('NS', [])) or 'None'}",
        "",
        "## 3. Infrastructure (Shodan)",
    ]

    if shodan_results:
        for ip_key, sd in shodan_results.items():
            ip = ip_key.replace("shodan_", "")
            if "error" in sd:
                lines.append(f"- **{ip}:** {sd['error']}")
            else:
                lines.append(f"- **{ip}** — Org: {sd.get('org','?')} | "
                             f"OS: {sd.get('os','?')} | "
                             f"Ports: {sd.get('ports', [])} | "
                             f"Country: {sd.get('country','?')}")
                if sd.get("vulns"):
                    lines.append(f"  - ⚠ Known CVEs: {', '.join(sd['vulns'])}")
    else:
        lines.append("- No Shodan data collected.")

    lines += [
        "",
        "## 4. SSL Certificate Intelligence (crt.sh)",
        f"- **Subdomains discovered:** {len(certs)}",
    ]
    if certs:
        lines.append("- **Sample subdomains:**")
        for c in certs[:10]:
            lines.append(f"  - `{c}`")

    lines += [
        "",
        "## 5. GitHub Presence",
        f"- **Public repos found:** {len(github)}",
    ]
    for r in github[:5]:
        lines.append(
            f"  - [{r['name']}]({r['url']}) — "
            f"{r.get('language','N/A')} | ⭐ {r.get('stars', 0)}"
        )

    lines += [
        "",
        "## 6. Entity Relationship Graph",
        "Graph data has been written to Neo4j AuraDB.",
        "Relationships modelled:",
        "- `Organization -[OWNS]-> Domain`",
        "- `Domain -[RESOLVES_TO]-> IP`",
        "- `Domain -[HAS_CERT]-> Certificate`",
        "",
        "---",
        "",
        "## Methodology",
        "| Step | Source | Tool/API |",
        "|------|--------|----------|",
        "| 1 | Domain registration | python-whois |",
        "| 2 | DNS enumeration | dnspython |",
        "| 3 | SSL transparency | crt.sh public API |",
        "| 4 | Infrastructure scan | Shodan free API |",
        "| 5 | Code repositories | GitHub REST API |",
        "| 6 | Graph modelling | Neo4j AuraDB (Cypher) |",
        "",
        "*All data collected from publicly available, open-source sources only.*",
        "*No private, restricted, or authenticated data was accessed.*",
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[+] Report saved: {filename}")
    return filename
