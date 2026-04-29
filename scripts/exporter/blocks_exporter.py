import json
import os
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

MC = Namespace("http://rpcw.di.uminho.pt/2026/minecraft/")

def export_blocks():
    g = Graph()
    g.bind("", MC)
    
    with open('../../data/1.21.11/blocks.json', 'r', encoding='utf-8') as f:
        blocks = json.load(f)
    with open('../../data/1.21.11/items.json', 'r', encoding='utf-8') as f:
        items = json.load(f)
        
    item_id_to_uri = {i['id']: MC[i['name']] for i in items}
        
    for b in blocks:
        block_name = b['name']
        uri = MC[block_name]
        
        g.add((uri, RDF.type, MC.Block))
        
        # --- Basic Data Properties ---
        g.add((uri, MC.hasID, Literal(b['id'], datatype=XSD.integer)))
        g.add((uri, MC.hasName, Literal(block_name, datatype=XSD.string)))
        g.add((uri, MC.hasDisplayName, Literal(b['displayName'], datatype=XSD.string)))
        g.add((uri, MC.hardness, Literal(b.get('hardness', 0.0), datatype=XSD.float)))
        g.add((uri, MC.blastResistance, Literal(b.get('resistance', 0.0), datatype=XSD.float)))
        
        # --- Booleans & Integers ---
        if 'stackSize' in b: g.add((uri, MC.stackSize, Literal(b['stackSize'], datatype=XSD.integer)))
        if 'diggable' in b: g.add((uri, MC.isDiggable, Literal(b['diggable'], datatype=XSD.boolean)))
        if 'transparent' in b: g.add((uri, MC.isTransparent, Literal(b['transparent'], datatype=XSD.boolean)))
        if 'emitLight' in b: g.add((uri, MC.emitLight, Literal(b['emitLight'], datatype=XSD.integer)))
        if 'filterLight' in b: g.add((uri, MC.filterLight, Literal(b['filterLight'], datatype=XSD.integer)))
        
        # --- NEW: Bounding Box & Material ---
        if 'boundingBox' in b: g.add((uri, MC.boundingBox, Literal(b['boundingBox'], datatype=XSD.string)))
        if 'material' in b: g.add((uri, MC.materialCategory, Literal(b['material'], datatype=XSD.string)))
            
        # --- NEW: State IDs ---
        if 'minStateId' in b: g.add((uri, MC.minStateId, Literal(b['minStateId'], datatype=XSD.integer)))
        if 'maxStateId' in b: g.add((uri, MC.maxStateId, Literal(b['maxStateId'], datatype=XSD.integer)))
        if 'defaultState' in b: g.add((uri, MC.defaultStateId, Literal(b['defaultState'], datatype=XSD.integer)))

        # --- NEW: Nested States Array ---
        if 'states' in b:
            for state in b['states']:
                # Create a unique URI for the state, e.g., :podzol_state_snowy
                state_uri = MC[f"{block_name}_state_{state['name']}"]
                
                # Classify and add properties to the state
                g.add((state_uri, RDF.type, MC.BlockState))
                g.add((state_uri, MC.hasName, Literal(state['name'], datatype=XSD.string)))
                g.add((state_uri, MC.BlockStateType, Literal(state['type'], datatype=XSD.string)))
                if 'num_values' in state:
                    g.add((state_uri, MC.BlockStateNumValues, Literal(state['num_values'], datatype=XSD.integer)))
                
                # Link the block to this specific state
                g.add((uri, MC.hasBlockState, state_uri))

        # --- Relations: Drops & Tools ---
        for drop_id in b.get('drops', []):
            if drop_id in item_id_to_uri:
                g.add((uri, MC.minedDrops, item_id_to_uri[drop_id]))
                
        for tool_id_str in b.get('harvestTools', {}).keys():
            tool_id = int(tool_id_str)
            if tool_id in item_id_to_uri:
                g.add((uri, MC.minedWith, item_id_to_uri[tool_id]))

    g.serialize('../ontology/data_blocks.ttl', format='turtle')
    print(f"Exported {len(blocks)} blocks with their states.")

if __name__ == "__main__":
    export_blocks()