import dns.resolver

def get_dns_records(domain):
    """
    Enumerate DNS records for a domain.
    Returns dict with A, MX, NS, TXT lists (empty list if record type absent).
    MX records are cleaned of trailing dots.
    """
    results = {}
    for record_type in ["A", "MX", "NS", "TXT"]:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            if record_type == "MX":
                # MX answers include priority — extract just the hostname
                results[record_type] = [str(r.exchange).rstrip(".") for r in answers]
            else:
                results[record_type] = [str(r).rstrip(".") for r in answers]
        except Exception:
            results[record_type] = []
    return results
