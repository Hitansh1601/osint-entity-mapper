# OSINT Intelligence Report
**Target:** `python.org`  
**Generated:** 2026-04-19 14:47:11  
**Analyst:** Hitansh Waghela  
**Confidence:** Medium-High (5 automated sources)

---

## Executive Summary
Automated OSINT investigation of `python.org` aggregating data from WHOIS registration records, DNS enumeration, SSL certificate transparency logs (crt.sh), Shodan infrastructure scanning, and GitHub repository discovery.

---

## 1. WHOIS Registration Data
- **Registrar:** Gandi SAS
- **Organization:** Unknown
- **Country:** Unknown
- **Created:** 1995-03-27 05:00:00+00:00
- **Contact Emails:** abuse@support.gandi.net

## 2. DNS Records
- **A Records (IPs):** 151.101.128.223, 151.101.0.223, 151.101.64.223, 151.101.192.223
- **MX Records:** mail.python.org
- **NS Records:** ns-1134.awsdns-13.org, ns-484.awsdns-60.com, ns-2046.awsdns-63.co.uk, ns-981.awsdns-58.net

## 3. Infrastructure (Shodan)
- **151.101.128.223:** Access denied (403 Forbidden)
- **151.101.0.223:** Access denied (403 Forbidden)
- **151.101.64.223:** Access denied (403 Forbidden)
- **151.101.192.223:** Access denied (403 Forbidden)

## 4. SSL Certificate Intelligence (crt.sh)
- **Subdomains discovered:** 0

## 5. GitHub Presence
- **Public repos found:** 10
  - [cpython](https://github.com/python/cpython) — Python | ⭐ 72378
  - [mypy](https://github.com/python/mypy) — Python | ⭐ 20380
  - [python-docs-ja](https://github.com/python/python-docs-ja) — Makefile | ⭐ 72
  - [peps](https://github.com/python/peps) — reStructuredText | ⭐ 4906
  - [typing_extensions](https://github.com/python/typing_extensions) — Python | ⭐ 561

## 6. Entity Relationship Graph
Graph data has been written to Neo4j AuraDB.
Relationships modelled:
- `Organization -[OWNS]-> Domain`
- `Domain -[RESOLVES_TO]-> IP`
- `Domain -[HAS_CERT]-> Certificate`

---

## Methodology
| Step | Source | Tool/API |
|------|--------|----------|
| 1 | Domain registration | python-whois |
| 2 | DNS enumeration | dnspython |
| 3 | SSL transparency | crt.sh public API |
| 4 | Infrastructure scan | Shodan free API |
| 5 | Code repositories | GitHub REST API |
| 6 | Graph modelling | Neo4j AuraDB (Cypher) |

*All data collected from publicly available, open-source sources only.*
*No private, restricted, or authenticated data was accessed.*