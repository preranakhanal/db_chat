
from django.db import connections
from django.conf import settings
from django.db.utils import OperationalError

def ensure_dynamic_registered(alias="dynamic"):
    if alias not in settings.DATABASES:
        params = {
            "NAME": "smis_ai_db",
            "USER": "smis_aiuser",
            "PASSWORD": "smisai",
            "HOST": "myschool.smis.online",
            "PORT": 6464,
        }
        register_database(alias, params)

def register_database(alias, params):
    settings.DATABASES[alias] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": params.get("NAME", "smis_ai_db"),
        "USER": params.get("USER", "smis_aiuser"),
        "PASSWORD": params.get("PASSWORD", "smisai"),
        "HOST": params.get("HOST", "myschool.smis.online"),
        "PORT": params.get("PORT", 6464),
        "OPTIONS": {
            "sslmode": "disable"
        },
        "TIME_ZONE": getattr(settings, "TIME_ZONE", None),
        "ATOMIC_REQUESTS": False,
        "CONN_HEALTH_CHECKS": False,
        "CONN_MAX_AGE": 0,
        "AUTOCOMMIT": True,
    }

def test_connection(alias="dynamic"):
    try:
        connections[alias].cursor()
        return True
    except OperationalError:
        return False

def get_schema(alias="dynamic"):
    ensure_dynamic_registered(alias)
    sql = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema='public';
    """
    with connections[alias].cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()

def run_sql(sql, alias="dynamic"):
    ensure_dynamic_registered(alias)
    with connections[alias].cursor() as cursor:
        cursor.execute(sql)
        cols = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return [dict(zip(cols, row)) for row in rows]
