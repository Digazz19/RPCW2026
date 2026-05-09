import re

LOCAL_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

XSD_TYPES = {
    "string": "xsd:string",
    "integer": "xsd:integer",
    "float": "xsd:float",
    "boolean": "xsd:boolean",
}


def is_valid_local_name(value):
    return bool(value and LOCAL_NAME_RE.match(value))


def require_local_name(value, field_name):
    value = (value or "").strip()

    if not is_valid_local_name(value):
        raise ValueError(f"{field_name} inválido.")

    return value


def sparql_literal(value, datatype):
    value = (value or "").strip()

    if datatype not in XSD_TYPES:
        raise ValueError("Tipo de literal inválido.")

    if datatype == "integer":
        int(value)
        return f'"{value}"^^xsd:integer'

    if datatype == "float":
        float(value)
        return f'"{value}"^^xsd:float'

    if datatype == "boolean":
        lowered = value.lower()
        if lowered not in {"true", "false"}:
            raise ValueError("Booleano deve ser true ou false.")
        return f'"{lowered}"^^xsd:boolean'

    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"^^xsd:string'