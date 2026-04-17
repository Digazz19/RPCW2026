from flask import Blueprint, render_template, request
from services.graphdb_client import run_select
from services.queries import (
    get_recipe_ingredients_query,
    get_mobs_that_drop_item_query,
    get_biomes_for_mob_query,
    get_tool_for_block_query,
    get_items_for_enchantment_query
)

competency_bp = Blueprint("competency", __name__)

@competency_bp.route("/", methods=["GET", "POST"])
def competency():
    result = None
    selected_query = None
    input_value = None

    if request.method == "POST":
        selected_query = request.form.get("query_type")
        input_value = request.form.get("input_value")

        if selected_query == "ingredients":
            result = run_select(get_recipe_ingredients_query(input_value))
        elif selected_query == "drops":
            result = run_select(get_mobs_that_drop_item_query(input_value))
        elif selected_query == "biomes":
            result = run_select(get_biomes_for_mob_query(input_value))
        elif selected_query == "tool":
            result = run_select(get_tool_for_block_query(input_value))
        elif selected_query == "enchantment":
            result = run_select(get_items_for_enchantment_query(input_value))

    return render_template(
        "competency.html",
        result=result,
        selected_query=selected_query,
        input_value=input_value
    )