from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.graphdb_client import run_update
from config import PREFIXES

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/add-relation", methods=["GET", "POST"])
def add_relation():
    message = None

    if request.method == "POST":
        subject = request.form.get("subject")
        predicate = request.form.get("predicate")
        obj = request.form.get("object")

        update_query = PREFIXES + f"""
        INSERT DATA {{
          mc:{subject} mc:{predicate} mc:{obj} .
        }}
        """

        try:
            run_update(update_query)
            message = "Relação adicionada com sucesso."
        except Exception as e:
            message = f"Erro: {e}"

    return render_template("add_relation.html", message=message)