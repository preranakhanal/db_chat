import os
from openai import OpenAI

api_key = "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"

client = OpenAI(api_key=api_key)

def pick_relevant_tables(user_query, schema):
    """Use LLM to pick only the relevant tables from the schema."""
    all_tables = sorted({t for t, c, d in schema})

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # faster/cheaper for table picking
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that selects only the database tables needed "
                    "to answer a query.\n"
                    f"Available tables: {', '.join(all_tables)}\n"
                    "Return only table names separated by commas, no explanations."
                )
            },
            {"role": "user", "content": user_query}
        ]
    )

    picked = response.choices[0].message.content
    selected = [t.strip() for t in picked.split(",") if t.strip() in all_tables]

    if not selected:
        selected = all_tables[:2]  # fallback, never empty

    return selected


def generate_sql(user_query, schema):
    if not user_query:
        user_query = ""
    print(f"User query: {user_query}")

    # Step 1: filter schema
    relevant_tables = pick_relevant_tables(user_query, schema)

    # Step 2: only include relevant tables in schema string
    schema_str = "\n".join([
        f"{t}.{c} ({d})" for t, c, d in schema if t in relevant_tables
    ])

    # Step 3: generate SQL
    response = client.chat.completions.create(
        model="gpt-4o",  # stronger for SQL generation
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a SQL generator. Schema:\n{schema_str}\n"
                    "Only output SELECT queries."
                )
            },
            {"role": "user", "content": user_query}
        ]
    )

    sql_response = response.choices[0].message.content.strip()

    # Step 4: clean SQL (remove ``` markers)
    if sql_response.startswith("```sql") and sql_response.endswith("```"):
        sql_response = sql_response[6:-3].strip()
    elif sql_response.startswith("```") and sql_response.endswith("```"):
        sql_response = sql_response[3:-3].strip()

    print(f"Cleaned SQL response: {sql_response}")

    return sql_response
