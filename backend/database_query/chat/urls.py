from django.urls import path
from . import views

urlpatterns = [
    path("connect/", views.connect_db, name="connect_db"),
    path("query/", views.query_db, name="query_db"),
    path("schema/", views.schema_view, name="schema"),
]
