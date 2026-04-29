import json
import os
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

MC = Namespace("http://rpcw.di.uminho.pt/2026/minecraft/")

def export_biomes():
    g = Graph()
    g.bind("", MC)
    
    with open('../../data/1.21.11/biomes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for b in data:
        uri = MC[b['name']]
        g.add((uri, RDF.type, MC.Biome))
        dimension = b.get('dimension', '').lower()
        if dimension == 'overworld': g.add((uri, RDF.type, MC.OverworldBiome))
        elif dimension == 'nether': g.add((uri, RDF.type, MC.NetherBiome))
        elif dimension == 'end': g.add((uri, RDF.type, MC.EndBiome))
        g.add((uri, MC.hasID, Literal(b['id'], datatype=XSD.integer)))
        g.add((uri, MC.hasName, Literal(b['name'], datatype=XSD.string)))
        g.add((uri, MC.hasDisplayName, Literal(b['displayName'], datatype=XSD.string)))
        
        if 'category' in b: g.add((uri, MC.biomeCategory, Literal(b['category'], datatype=XSD.string)))
        if 'temperature' in b: g.add((uri, MC.temperature, Literal(b['temperature'], datatype=XSD.float)))
        if 'has_precipitation' in b: g.add((uri, MC.hasPrecipitation, Literal(b['has_precipitation'], datatype=XSD.boolean)))

    g.serialize('../ontology/data_biomes.ttl', format='turtle')
    print(f"Exported {len(data)} biomes.")

if __name__ == "__main__":
    export_biomes()