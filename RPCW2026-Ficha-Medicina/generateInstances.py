import re
import pandas as pd
from rdflib import Graph, Namespace, RDF, Literal

BASE = "http://www.example.org/disease-ontology#"
ONT = Namespace(BASE)

g = Graph()
g.parse("medical.ttl", format="turtle")
g.bind("", ONT)

for s, _, o in list(g.triples((None, ONT.name, None))):
    g.remove((s, ONT.name, o))
    g.add((s, ONT.nome, o))

def disease_uri(name):
    name = re.sub(r"[^a-zA-Z0-9 ]", "", name.strip())
    return ONT["_".join(w.capitalize() for w in name.split())]

def symptom_uri(name):
    name = re.sub(r"[^a-zA-Z0-9 _]", "", name.strip())
    return ONT["".join(w.capitalize() for w in re.split(r"[ _]+", name) if w)]

df = pd.read_csv("Disease_Syntoms.csv")
symptom_cols = [c for c in df.columns if c.startswith("Symptom")]

for _, row in df.iterrows():
    d = disease_uri(row["Disease"])
    g.add((d, RDF.type, ONT.Disease))
    for col in symptom_cols:
        if pd.notna(row[col]):
            s = symptom_uri(row[col])
            g.add((s, RDF.type, ONT.Symptom))
            g.add((d, ONT.hasSymptom, s))

df_desc = pd.read_csv("Disease_Description.csv")

for _, row in df_desc.iterrows():
    d = disease_uri(row["Disease"])
    g.add((d, ONT.hasDescription, Literal(row["Description"])))

# Passo 5 — guardar
g.serialize("med_doencas.ttl", format="turtle")
print("Ontologia povoada criada: med_doencas.ttl")