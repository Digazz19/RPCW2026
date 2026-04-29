import json
import os
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

MC = Namespace("http://rpcw.di.uminho.pt/2026/minecraft/")

def export_foods():
    g = Graph()
    g.bind("", MC)
    
    with open('../../data/1.21.11/foods.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for f_item in data:
        uri = MC[f_item['name']]
        food_type = f_item.get('displayName', 'generic')
        if food_type.startswith('Cooked'):
            g.add((uri, RDF.type, MC.CookedFood))
        elif food_type.startswith('Raw'):
            g.add((uri, RDF.type, MC.RawFood))
        else:
            g.add((uri, RDF.type, MC.Food))
        # Assuming food properties, adapt based on exact JSON structure
        g.add((uri, MC.hasID, Literal(f_item['id'], datatype=XSD.integer)))
        g.add((uri, MC.hasName, Literal(f_item['name'], datatype=XSD.string)))
        g.add((uri, MC.hasDisplayName, Literal(f_item['displayName'], datatype=XSD.string)))
        
        if 'foodPoints' in f_item:
            g.add((uri, MC.foodPoints, Literal(f_item['foodPoints'], datatype=XSD.float)))
        if 'saturation' in f_item:
            g.add((uri, MC.saturation, Literal(f_item['saturation'], datatype=XSD.float)))
        if 'saturationRatio' in f_item:
            g.add((uri, MC.saturationRatio, Literal(f_item['saturationRatio'], datatype=XSD.float)))
        if 'effectiveQuality' in f_item:
            g.add((uri, MC.effectiveQuality, Literal(f_item['effectiveQuality'], datatype=XSD.float)))

    g.serialize('../ontology/data_foods.ttl', format='turtle')
    print(f"Exported {len(data)} foods.")

if __name__ == "__main__":
    export_foods()