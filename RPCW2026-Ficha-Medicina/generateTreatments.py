import re
import pandas as pd
from rdflib import Graph, Namespace, RDF

BASE = "http://www.example.org/disease-ontology#"
ONT = Namespace(BASE)

g = Graph()
g.parse("med_doencas.ttl", format="turtle")
g.bind("", ONT)

def disease_uri(name):
    name = re.sub(r"[^a-zA-Z0-9 ]", "", name.strip())
    return ONT["_".join(w.capitalize() for w in name.split())]

def treatment_uri(name):
    name = re.sub(r"[^a-zA-Z0-9 _]", "", name.strip())
    return ONT["".join(w.capitalize() for w in re.split(r"[ _]+", name) if w)]

df = pd.read_csv("Disease_Treatment.csv")
treatment_cols = [c for c in df.columns if c.startswith("Precaution")]

for _, row in df.iterrows():
    d = disease_uri(row["Disease"])
    for col in treatment_cols:
        if pd.notna(row[col]):
            t = treatment_uri(row[col])
            g.add((t, RDF.type, ONT.Treatment))
            g.add((d, ONT.hasTreatment, t))

g.serialize("med_tratamentos.ttl", format="turtle")
print("Ontologia povoada criada: med_tratamentos.ttl")