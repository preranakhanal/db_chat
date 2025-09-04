import os
from openai import OpenAI

api_key = "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"

client = OpenAI(api_key=api_key)

def generate_sql(user_query, schema):
    if not user_query:
        user_query = ""
    print(f"User query: {user_query}")
    schema_str = "\n".join([f"{t}.{c} ({d})" for t, c, d in schema])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"You are a SQL generator. Schema:\n{schema_str}\nOnly output SELECT queries."
            },
            {"role": "user", "content": user_query}
        ]
    )
    sql_response = response.choices[0].message.content.strip()
    # Remove code block markers if present
    if sql_response.startswith("```sql") and sql_response.endswith("```"):
        sql_response = sql_response[6:-3].strip()
    elif sql_response.startswith("```") and sql_response.endswith("```"):
        sql_response = sql_response[3:-3].strip()
    
    print (f"Cleaned SQL response: {sql_response}")
        
    return sql_response
