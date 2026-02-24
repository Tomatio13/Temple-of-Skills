CREATE TABLE IF NOT EXISTS qa_entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  summary TEXT NOT NULL,
  keywords TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_qa_entries_question ON qa_entries(question);
CREATE INDEX IF NOT EXISTS idx_qa_entries_answer ON qa_entries(answer);
CREATE INDEX IF NOT EXISTS idx_qa_entries_summary ON qa_entries(summary);
CREATE INDEX IF NOT EXISTS idx_qa_entries_keywords ON qa_entries(keywords);
