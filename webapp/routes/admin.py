from flask import Blueprint, render_template, request

from config import PREFIXES
from services.graphdb_client import run_select, run_update, run_ask
from services.queries import (
    get_insertable_properties_query,
    ask_resource_exists_query,
    ask_property_exists_query,
)
from services.validation import require_local_name, sparql_literal

admin_bp = Blueprint("admin", __name__)


def local_name(uri):
    return str(uri).rstrip("/").split("/")[-1]


@admin_bp.route("/add-relation", methods=["GET", "POST"])
def add_relation():
    message = None

    properties_result = run_select(get_insertable_properties_query())
    properties = []

    for row in properties_result.get("results", {}).get("bindings", []):
        prop_uri = row["property"]["value"]
        prop_type = row["type"]["value"]

        properties.append({
            "name": local_name(prop_uri),
            "type": local_name(prop_type),
        })

    if request.method == "POST":
        try:
            subject = require_local_name(request.form.get("subject"), "Sujeito")
            predicate = require_local_name(request.form.get("predicate"), "Predicado")
            object_kind = request.form.get("object_kind")
            object_value = request.form.get("object")
            literal_type = request.form.get("literal_type", "string")

            if not run_ask(ask_property_exists_query(predicate)):
                raise ValueError("Predicado não existe como ObjectProperty ou DatatypeProperty.")

            if object_kind == "resource":
                obj = require_local_name(object_value, "Objeto")
                object_expr = f"mc:{obj}"
            elif object_kind == "literal":
                object_expr = sparql_literal(object_value, literal_type)
            else:
                raise ValueError("Tipo de objeto inválido.")

            update_query = PREFIXES + f"""
            INSERT DATA {{
              mc:{subject} mc:{predicate} {object_expr} .
            }}
            """

            run_update(update_query)
            message = "Triple inserida com sucesso."

        except Exception as e:
            message = f"Erro: {e}"

    return render_template(
        "add_relation.html",
        message=message,
        properties=properties,
    )