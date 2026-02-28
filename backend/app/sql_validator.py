"""
SQL validation and sanitization for LLM-generated queries.
Only allows safe SELECT statements; blocks DDL/DML and injection patterns.
"""

import re

# Keywords that must not appear (case-insensitive)
FORBIDDEN_KEYWORDS = frozenset(
    {
        "drop",
        "delete",
        "update",
        "insert",
        "truncate",
        "alter",
        "create",
        "replace",
        "exec",
        "execute",
        "grant",
        "revoke",
        "commit",
        "rollback",
        "lock",
        "unlock",
        "load_file",
        "into outfile",
        "into dumpfile",
        "information_schema",
        "mysql.",
        "benchmark(",
        "sleep(",
        "union select",
    }
)

# Statement must be a single SELECT (we allow only the first statement)
SELECT_PATTERN = re.compile(r"^\s*select\b", re.IGNORECASE | re.DOTALL)


def is_safe_sql(sql: str) -> bool:
    """
    Return True if the SQL is considered safe to execute:
    - Must start with SELECT (after optional whitespace).
    - Must not contain forbidden keywords or patterns.
    - Should not contain multiple statements (no semicolon followed by more SQL).
    """
    if not sql or not sql.strip():
        return False
    normalized = " " + sql.lower() + " "
    # Must start with SELECT
    if not SELECT_PATTERN.match(sql.strip()):
        return False
    # No forbidden keywords (as whole words where sensible)
    for word in FORBIDDEN_KEYWORDS:
        # Match word boundaries so "information_schema" matches
        if word in normalized:
            return False
    # Disallow multiple statements: semicolon then non-whitespace
    if re.search(r";\s*\S", sql):
        return False
    return True


def get_single_statement(sql: str) -> str:
    """Return the first statement only (before any semicolon)."""
    idx = sql.find(";")
    if idx >= 0:
        return sql[:idx].strip()
    return sql.strip()
