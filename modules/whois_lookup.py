import whois

def get_whois_data(domain):
    """
    Fetch WHOIS registration data for a domain.
    Handles whois library quirks: creation_date can be a list,
    emails can be a string or list.
    """
    try:
        w = whois.whois(domain)

        # creation_date is often a list — take the first entry
        if isinstance(w.creation_date, list):
            creation_date = str(w.creation_date[0])
        elif w.creation_date:
            creation_date = str(w.creation_date)
        else:
            creation_date = "Unknown"

        # emails can be a string (not a list) — normalise to list
        if isinstance(w.emails, list):
            emails = list(set(w.emails))
        elif isinstance(w.emails, str):
            emails = [w.emails]
        else:
            emails = []

        return {
            "registrar": str(w.registrar) if w.registrar else "Unknown",
            "org": str(w.org) if w.org else "Unknown",
            "country": str(w.country) if w.country else "Unknown",
            "creation_date": creation_date,
            "emails": emails
        }
    except Exception as e:
        return {"error": str(e)}
