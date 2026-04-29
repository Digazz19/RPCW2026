import json
import os
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

MC = Namespace("http://rpcw.di.uminho.pt/2026/minecraft/")

def export_items():
    g = Graph()
    g.bind("", MC)
    
    with open('../../data/1.21.11/items.json', 'r', encoding='utf-8') as f:
        items = json.load(f)
    with open('../../data/1.21.11/enchantments.json', 'r', encoding='utf-8') as f:
        enchantments = json.load(f)

    # Group enchantments by category
    ench_by_cat = {}
    for e in enchantments:
        if 'category' in e:
            ench_by_cat.setdefault(e['category'], []).append(MC[e['name']])

    for i in items:
        uri = MC[i['name']]
        g.add((uri, RDF.type, MC.Item))
        g.add((uri, MC.hasID, Literal(i['id'], datatype=XSD.integer)))
        g.add((uri, MC.hasName, Literal(i['name'], datatype=XSD.string)))
        g.add((uri, MC.hasDisplayName, Literal(i['displayName'], datatype=XSD.string)))
        
        if 'stackSize' in i:
            g.add((uri, MC.stackSize, Literal(i['stackSize'], datatype=XSD.integer)))
        if 'maxDurability' in i:
            g.add((uri, MC.maxDurability, Literal(i['maxDurability'], datatype=XSD.integer)))
            
        categories = i.get('enchantCategories', [])
        if 'weapon' in categories or 'melee_weapon' in categories: g.add((uri, RDF.type, MC.Weapon))
        if 'mining' in categories: g.add((uri, RDF.type, MC.Tool))
        if 'armor' in categories: g.add((uri, RDF.type, MC.Armor))
            
        for cat in categories:
            for ench_uri in ench_by_cat.get(cat, []):
                g.add((uri, MC.canBeEnchantedWith, ench_uri))

        repairs = i.get('repairs', [])
        for r in repairs:
            g.add((uri, MC.canBeRepairedWith, MC[r]))

    g.serialize('../ontology/data_items.ttl', format='turtle')
    print(f"Exported {len(items)} items.")

if __name__ == "__main__":
    export_items()