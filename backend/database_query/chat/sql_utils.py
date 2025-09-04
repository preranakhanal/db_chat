def validate_sql(sql, schema):
    
    print(f"Validating SQL: {sql}")
    
    if not sql.upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")
    # Allow a single trailing semicolon, but block multiple statements
    semicolon_count = sql.count(";")
    if semicolon_count > 1 or (semicolon_count == 1 and not sql.strip().endswith(";")):
        raise ValueError("Multiple statements not allowed")

    valid_names = {t for t, c, d in schema} | {c for t, c, d in schema}
    sql_keywords = {
        "select", "from", "where", "as", "distinct", "count", "on", "join", "left", "right", "inner", "outer",
        "group", "by", "order", "limit", "offset", "having", "and", "or", "not", "in", "is", "null", "like", "between",
        "case", "when", "then", "else", "end", "union", "all", "exists", "asc", "desc", "top", "now", "interval"
    }
    # Add aliases defined with AS to valid_names
    import re
    aliases = set(re.findall(r"AS\s+([a-zA-Z_][a-zA-Z0-9_]*)", sql, re.IGNORECASE))
    valid_names |= aliases
    for word in sql.replace("(", " ").replace(")", " ").replace(",", " ").split():
        if word.isidentifier() and word.lower() not in map(str.lower, valid_names) and word.lower() not in sql_keywords:
            raise ValueError(f"Unknown identifier: {word}")
