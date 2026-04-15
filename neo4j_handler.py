from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class Neo4jHandler:
    """
    Handles all Neo4j AuraDB operations for the OSINT entity mapper.
    Uses MERGE throughout to prevent duplicate nodes on re-runs.
    Connection errors are surfaced immediately with clear messages.
    """

    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(
                NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
            )
            # Verify connectivity immediately
            self.driver.verify_connectivity()
        except AuthError:
            raise RuntimeError(
                "[!] Neo4j authentication failed.\n"
                "    Check NEO4J_USER and NEO4J_PASSWORD in config.py"
            )
        except ServiceUnavailable:
            raise RuntimeError(
                "[!] Neo4j instance unreachable.\n"
                "    Check NEO4J_URI in config.py and ensure AuraDB instance is running."
            )

    def close(self):
        self.driver.close()

    def _run(self, query, **params):
        """Internal helper — runs a Cypher query in a session."""
        with self.driver.session() as session:
            session.run(query, **params)

    def create_domain_node(self, domain):
        self._run("MERGE (d:Domain {name: $domain})", domain=domain)

    def create_ip_node(self, ip):
        self._run("MERGE (i:IP {address: $ip})", ip=ip)

    def create_org_node(self, org_name):
        self._run("MERGE (o:Organization {name: $org})", org=org_name)

    def link_domain_to_ip(self, domain, ip):
        self._run("""
            MATCH (d:Domain {name: $domain})
            MATCH (i:IP {address: $ip})
            MERGE (d)-[:RESOLVES_TO]->(i)
        """, domain=domain, ip=ip)

    def link_org_to_domain(self, org, domain):
        self._run("""
            MATCH (o:Organization {name: $org})
            MATCH (d:Domain {name: $domain})
            MERGE (o)-[:OWNS]->(d)
        """, org=org, domain=domain)

    def link_domain_to_cert(self, domain, cert_domain):
        self._run("""
            MATCH (d:Domain {name: $domain})
            MERGE (c:Certificate {domain: $cert})
            MERGE (d)-[:HAS_CERT]->(c)
        """, domain=domain, cert=cert_domain)
