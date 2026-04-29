import json
import os
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

MC = Namespace("http://rpcw.di.uminho.pt/2026/minecraft/")

def export_effects():
    g = Graph()
    g.bind("", MC)
    
    with open('../../data/1.21.11/effects.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for e in data:
        uri = MC[e['name'].replace(" ", "_")]
        
        if e['type'] == 'good':
            g.add((uri, RDF.type, MC.BeneficialEffect))
        elif e['type'] == 'bad':
            g.add((uri, RDF.type, MC.HarmfulEffect))
        else:
            g.add((uri, RDF.type, MC.Effect))
            
        g.add((uri, MC.hasID, Literal(e['id'], datatype=XSD.integer)))
        g.add((uri, MC.hasName, Literal(e['name'], datatype=XSD.string)))
        g.add((uri, MC.hasDisplayName, Literal(e['displayName'], datatype=XSD.string)))

    g.serialize('../ontology/data_effects.ttl', format='turtle')
    print(f"Exported {len(data)} effects.")

if __name__ == "__main__":
    export_effects()