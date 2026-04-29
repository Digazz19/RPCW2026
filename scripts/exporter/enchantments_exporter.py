import json
import os
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

MC = Namespace("http://rpcw.di.uminho.pt/2026/minecraft/")

def export_enchantments():
    g = Graph()
    g.bind("", MC)
    
    with open('../../data/1.21.11/enchantments.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for e in data:
        uri = MC[e['name']]
        type = e.get('category', 'generic')
        #type defines categories like ArmorEnchantment, WeaponEnchantment, etc. We can use it as a class if needed.
        g.add((uri, RDF.type, MC[type.capitalize() + "Enchantment"]))
        #g.add((uri, RDF.type, MC.Enchantment))
        g.add((uri, MC.hasID, Literal(e['id'], datatype=XSD.integer)))
        g.add((uri, MC.hasName, Literal(e['name'], datatype=XSD.string)))
        g.add((uri, MC.hasDisplayName, Literal(e['displayName'], datatype=XSD.string)))
        g.add((uri, MC.maxLevel, Literal(e['maxLevel'], datatype=XSD.integer)))
        g.add((uri, MC.enchantmentWeight, Literal(e['weight'], datatype=XSD.integer)))
        g.add((uri, MC.isCurse, Literal(e.get('curse', False), datatype=XSD.boolean)))
        g.add((uri, MC.isDiscoverable, Literal(e.get('discoverable', True), datatype=XSD.boolean)))
        g.add((uri, MC.isTradeable, Literal(e.get('tradeable', True), datatype=XSD.boolean)))
        g.add((uri, MC.isTreasureOnly, Literal(e.get('treasureOnly', False), datatype=XSD.boolean)))
        g.add((uri, MC.minCostA, Literal(e['minCost'].get('a', 0), datatype=XSD.integer)))
        g.add((uri, MC.minCostB, Literal(e['minCost'].get('b', 0), datatype=XSD.integer)))
        g.add((uri, MC.maxCostA, Literal(e['maxCost'].get('a', 0), datatype=XSD.integer)))
        g.add((uri, MC.maxCostB, Literal(e['maxCost'].get('b', 0), datatype=XSD.integer)))
        
        for excl in e.get('exclude', []):
            g.add((uri, MC.incompatibleWith, MC[excl]))

    os.makedirs('../ontology', exist_ok=True)
    g.serialize('../ontology/data_enchantments.ttl', format='turtle')
    print(f"Exported {len(data)} enchantments.")

if __name__ == "__main__":
    export_enchantments()