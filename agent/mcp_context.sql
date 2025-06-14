CREATE TABLE IF NOT EXISTS mcp_context (
    id SERIAL PRIMARY KEY,
    ticket_id TEXT UNIQUE NOT NULL,
    repo_url TEXT NOT NULL,
    branch_name TEXT,
    pr_url TEXT,
    status TEXT DEFAULT 'created',
    summary TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
