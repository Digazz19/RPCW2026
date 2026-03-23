import json
import re
from rdflib import Graph, Namespace, RDF, Literal

BASE = "http://www.example.org/disease-ontology#"
ONT = Namespace(BASE)

g = Graph()
g.parse("med_tratamentos.ttl", format="turtle")
g.bind("", ONT)

def symptom_uri(name):
    name = re.sub(r"[^a-zA-Z0-9 _]", "", name.strip())
    return ONT["".join(w.capitalize() for w in re.split(r"[ _]+", name) if w)]

with open("doentes.json", encoding="utf-8") as f:
    doentes = json.load(f)

for i, doente in enumerate(doentes, start=1):
    d = ONT[f"doente_{i:05d}"]
    g.add((d, RDF.type, ONT.Patient))
    g.add((d, ONT.nome, Literal(doente["nome"])))
    for sintoma in doente["sintomas"]:
        g.add((d, ONT.exhibitsSymptom, symptom_uri(sintoma)))

g.serialize("med_doentes.ttl", format="turtle")
print("Ontologia povoada criada: med_doentes.ttl")