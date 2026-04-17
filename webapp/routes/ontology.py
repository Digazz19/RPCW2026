from flask import Blueprint, render_template, request
from services.graphdb_client import run_select
from services.queries import (
    get_classes_query,
    get_instances_of_class_query,
    get_resource_details_query,
    get_resource_inverse_query
)

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
    direct = run_select(get_resource_details_query(resource_name))
    inverse = run_select(get_resource_inverse_query(resource_name))
    return render_template(
        "resource_detail.html",
        resource_name=resource_name,
        direct=direct["results"]["bindings"],
        inverse=inverse["results"]["bindings"]
    )