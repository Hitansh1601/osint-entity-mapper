"""
OSINT Entity Mapper
-------------------
Aggregates open-source intelligence on a target domain from 5 public sources
and models entity relationships in a Neo4j graph database.

Usage:
    python main.py <domain>
    python main.py github.com
"""

import sys
from modules.whois_lookup import get_whois_data
from modules.dns_lookup import get_dns_records
from modules.crtsh_lookup import get_crtsh_data
from modules.shodan_lookup import get_shodan_data
from modules.github_lookup import search_github_org
from neo4j_handler import Neo4jHandler
from report_generator import generate_report


def run_investigation(target_domain):
    print(f"\n{'='*50}")
    print(f"  OSINT ENTITY MAPPER")
    print(f"  Target: {target_domain}")
    print(f"{'='*50}\n")

    db = None
    report_data = {"target": target_domain, "sources": {}}

    try:
        db = Neo4jHandler()
        # ── 1. WHOIS ──────────────────────────────────────────
        print("[*] Running WHOIS lookup...")
        whois_data = get_whois_data(target_domain)
        report_data["sources"]["whois"] = whois_data

        db.create_domain_node(target_domain)

        org = whois_data.get("org", "")
        if org and org not in ("Unknown", "None", ""):
            db.create_org_node(org)
            db.link_org_to_domain(org, target_domain)
            print(f"    ↳ Org: {org}")

        # ── 2. DNS ────────────────────────────────────────────
        print("[*] Running DNS lookup...")
        dns_data = get_dns_records(target_domain)
        report_data["sources"]["dns"] = dns_data

        a_records = dns_data.get("A", [])
        print(f"    ↳ A records: {a_records}")

        for ip in a_records:
            db.create_ip_node(ip)
            db.link_domain_to_ip(target_domain, ip)

            # ── 3. SHODAN (per IP) ─────────────────────────
            print(f"[*] Running Shodan on {ip}...")
            shodan_data = get_shodan_data(ip)
            report_data["sources"][f"shodan_{ip}"] = shodan_data
            if "error" not in shodan_data:
                print(f"    ↳ Ports: {shodan_data.get('ports', [])}")

        # ── 4. crt.sh ─────────────────────────────────────────
        print("[*] Pulling SSL certificate data from crt.sh...")
        certs = get_crtsh_data(target_domain)
        report_data["sources"]["crtsh"] = certs
        print(f"    ↳ Subdomains found: {len(certs)}")

        for cert_domain in certs[:10]:
            db.link_domain_to_cert(target_domain, cert_domain)

        # ── 5. GITHUB ─────────────────────────────────────────
        print("[*] Searching GitHub...")
        # Use the second-level domain label (e.g. "github" from "github.com")
        parts = target_domain.replace("www.", "").split(".")
        org_guess = parts[0] if len(parts) >= 2 else target_domain
        github_data = search_github_org(org_guess)
        report_data["sources"]["github"] = github_data
        print(f"    ↳ Repos found: {len(github_data)}")

    finally:
        # Always close — even if an exception occurs mid-investigation
        if db is not None:
            db.close()

    # ── REPORT ────────────────────────────────────────────────
    print("\n[*] Generating intelligence report...")
    report_file = generate_report(report_data)

    print(f"\n{'='*50}")
    print(f"  [+] INVESTIGATION COMPLETE")
    print(f"  [+] Report: {report_file}")
    print(f"  [+] Graph: console.neo4j.io")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <domain>")
        print("Example: python main.py github.com")
        sys.exit(1)
    run_investigation(sys.argv[1])
