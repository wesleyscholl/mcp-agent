CREATE TABLE mcp_context (
  id SERIAL PRIMARY KEY,
  ticket_id TEXT UNIQUE,
  repo_url TEXT,
  branch_name TEXT,
  pr_url TEXT,
  status TEXT DEFAULT 'created',
  summary TEXT,
  description TEXT
);