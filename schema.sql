-- Phase 2: move from SQLite to Postgres + pgvector
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE research (
  id TEXT PRIMARY KEY, question TEXT NOT NULL, status TEXT NOT NULL,
  report TEXT, created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE sources (
  id SERIAL PRIMARY KEY, research_id TEXT REFERENCES research(id) ON DELETE CASCADE,
  url TEXT, title TEXT, domain TEXT, credibility INT, summary TEXT, key_points JSONB
);
CREATE TABLE chunks (  -- for RAG follow-up Q&A over a finished report
  id SERIAL PRIMARY KEY, source_id INT REFERENCES sources(id) ON DELETE CASCADE,
  content TEXT, embedding vector(1024)
);
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
