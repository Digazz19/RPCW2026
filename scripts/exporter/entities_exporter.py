import json
import os
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

MC = Namespace("http://rpcw.di.uminho.pt/2026/minecraft/")

def export_entities():
    g = Graph()
    g.bind("", MC)
    
    with open('../../data/1.21.11/entities.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for e in data:
        uri = MC[e['name']]
        
        cat = e.get('category', '').lower()
        ent_type = e.get('type', '').lower()
        if 'passive' in ent_type: g.add((uri, RDF.type, MC.PassiveMob))
        elif 'hostile' in ent_type: g.add((uri, RDF.type, MC.HostileMob))
        elif ent_type == 'projectile': g.add((uri, RDF.type, MC.ProjectileEntity))
        elif ent_type == 'mob': g.add((uri, RDF.type, MC.Mob))
        else: g.add((uri, RDF.type, MC.Entity))
            
        g.add((uri, MC.hasID, Literal(e['id'], datatype=XSD.integer)))
        g.add((uri, MC.hasName, Literal(e['name'], datatype=XSD.string)))
        g.add((uri, MC.hasDisplayName, Literal(e['displayName'], datatype=XSD.string)))
        
        if 'width' in e: g.add((uri, MC.entityWidth, Literal(e['width'], datatype=XSD.float)))
        if 'height' in e: g.add((uri, MC.entityHeight, Literal(e['height'], datatype=XSD.float)))

    g.serialize('../ontology/data_entities.ttl', format='turtle')
    print(f"Exported {len(data)} entities.")

if __name__ == "__main__":
    export_entities()