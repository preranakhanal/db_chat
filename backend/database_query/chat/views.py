from django.http import JsonResponse
from .db_utils import register_database, test_connection, get_schema, run_sql
from .services import generate_sql
from .sql_utils import validate_sql

def connect_db(request):
    """Register DB connection dynamically"""
    params = {
        "NAME": request.GET.get("name"),
        "USER": request.GET.get("user"),
        "PASSWORD": request.GET.get("password"),
        "HOST": request.GET.get("host"),
        "PORT": request.GET.get("port"),
    }
    alias = request.GET.get("alias", "dynamic")
    register_database(alias, params)
    success = test_connection(alias)
    return JsonResponse({"connected": success, "alias": alias})

def query_db(request):
    """Run natural language query"""
    user_query = request.GET.get("query")
    alias = request.GET.get("alias", "dynamic")

    schema = get_schema(alias)
    sql = generate_sql(user_query, schema)
    # validate_sql(sql, schema)
    result = run_sql(sql, alias)

    return JsonResponse({"sql": sql, "result": result})

def schema_view(request):
    """Return schema for connected DB"""
    alias = request.GET.get("alias", "dynamic")
    schema = get_schema(alias)
    return JsonResponse({"schema": schema})
