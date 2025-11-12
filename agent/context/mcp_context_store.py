import psycopg2
import os
from datetime import datetime



class MCPContextStore:
    def __init__(self, db_url: str):
        db_url = os.getenv("POSTGRES_URL")
        self.conn = psycopg2.connect(db_url)
        self.conn.autocommit = True

    def insert_or_update_context(self, ticket_id, repo_url, summary, description, branch_name=None, pr_url=None, status="created"):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO mcp_context (ticket_id, repo_url, branch_name, pr_url, status, summary, description, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticket_id)
                DO UPDATE SET
                    repo_url = EXCLUDED.repo_url,
                    branch_name = EXCLUDED.branch_name,
                    pr_url = EXCLUDED.pr_url,
                    status = EXCLUDED.status,
                    summary = EXCLUDED.summary,
                    description = EXCLUDED.description,
                    updated_at = EXCLUDED.updated_at;
            """, (
                ticket_id,
                repo_url,
                branch_name,
                pr_url,
                status,
                summary,
                description,
                datetime.utcnow(),
                datetime.utcnow()
            ))

    def get_context(self, ticket_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM mcp_context WHERE ticket_id = %s", (ticket_id,))
            row = cur.fetchone()
            if row:
                return dict(zip([desc[0] for desc in cur.description], row))
            return None

    def update_status(self, ticket_id, status):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE mcp_context
                SET status = %s, updated_at = %s
                WHERE ticket_id = %s
            """, (status, datetime.utcnow(), ticket_id))

    def update_pr_url(self, ticket_id, pr_url):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE mcp_context
                SET pr_url = %s, updated_at = %s
                WHERE ticket_id = %s
            """, (pr_url, datetime.utcnow(), ticket_id))
