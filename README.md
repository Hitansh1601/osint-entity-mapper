# OSINT Entity Mapper

> Automated open-source intelligence tool that aggregates domain intelligence 
> from 5 public sources and models entity relationships in a Neo4j graph database.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Neo4j](https://img.shields.io/badge/Neo4j-AuraDB-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## What It Does

Takes a target domain and automatically:
- Pulls WHOIS registration data (registrar, org, country, emails)
- Enumerates DNS records (A, MX, NS, TXT)
- Discovers subdomains via SSL certificate transparency (crt.sh)
- Fingerprints infrastructure via Shodan (open ports, OS, CVEs)
- Finds GitHub organization repositories
- Models all entity relationships in **Neo4j** graph database
- Generates a structured **markdown intelligence report**

## Data Sources (5)

| Source | Data Extracted | Method |
|--------|---------------|--------|
| WHOIS | Registrar, org, country, emails | python-whois |
| DNS | A, MX, NS, TXT records | dnspython |
| crt.sh | SSL subdomains (cert transparency) | Public API |
| Shodan | Open ports, OS, vulns, org | Shodan free API |
| GitHub | Public repositories, languages | GitHub REST API |

## Entity Relationship Model