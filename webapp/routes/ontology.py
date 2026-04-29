from flask import Blueprint, render_template, request
from services.graphdb_client import run_select
from services.queries import (
    get_classes_query,
    get_instances_of_class_query,
    get_resource_details_query,
    get_resource_inverse_query
)
from collections import defaultdict

ontology_bp = Blueprint("ontology", __name__)

def extract_local_name(uri: str) -> str:
    if "#" in uri:
        return uri.split("#")[-1]
    return uri.rstrip("/").split("/")[-1]

@ontology_bp.route("/classes")
def list_classes():
    data = run_select(get_classes_query())
    classes = [extract_local_name(b["class"]["value"]) for b in data["results"]["bindings"]]
    return render_template("classes.html", classes=classes)

@ontology_bp.route("/classes/<class_name>")
def class_detail(class_name):
    data = run_select(get_instances_of_class_query(class_name))
    instances = [extract_local_name(b["instance"]["value"]) for b in data["results"]["bindings"]]
    return render_template("class_detail.html", class_name=class_name, instances=instances)

@ontology_bp.route("/resource/<resource_name>")
def resource_detail(resource_name):
    page = int(request.args.get("page", 1))
    per_page = 25

    direct = run_select(get_resource_details_query(resource_name))
    inverse = run_select(get_resource_inverse_query(resource_name))

    direct_rows = direct["results"]["bindings"]
    inverse_rows = inverse["results"]["bindings"]

    def is_blank_node_value(value: str) -> bool:
        if not value:
            return False
        value = str(value)
        return value.startswith("node") or "/.well-known/genid/" in value

    # esconder blank nodes feios
    clean_direct = []
    for row in direct_rows:
        o_value = row.get("o", {}).get("value", "")
        if not is_blank_node_value(o_value):
            clean_direct.append(row)

    clean_inverse = []
    for row in inverse_rows:
        s_value = row.get("s", {}).get("value", "")
        if not is_blank_node_value(s_value):
            clean_inverse.append(row)

    # agrupar relações inversas por propriedade
    grouped_inverse = defaultdict(list)

    for row in clean_inverse:
        predicate = row["p"]["value"]
        grouped_inverse[predicate].append(row)

    grouped_inverse = dict(sorted(grouped_inverse.items(), key=lambda item: item[0]))

    # paginação por grupos
    group_items = list(grouped_inverse.items())
    total_groups = len(group_items)
    total_pages = max((total_groups + per_page - 1) // per_page, 1)

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    start = (page - 1) * per_page
    end = start + per_page

    paginated_groups = group_items[start:end]

    return render_template(
        "resource_detail.html",
        resource_name=resource_name,
        direct=clean_direct,
        inverse=clean_inverse,
        grouped_inverse=paginated_groups,
        page=page,
        total_pages=total_pages,
        total_inverse=len(clean_inverse)
    )

