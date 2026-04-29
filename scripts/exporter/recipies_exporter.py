import json
import os
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

MC = Namespace("http://rpcw.di.uminho.pt/2026/minecraft/")

def export_recipes():
    g = Graph()
    g.bind("", MC)
    
    with open('../../data/1.21.11/recipes.json', 'r', encoding='utf-8') as f:
        recipes_data = json.load(f)
    with open('../../data/1.21.11/items.json', 'r', encoding='utf-8') as f:
        items = json.load(f)
        
    item_id_to_uri = {i['id']: MC[i['name']] for i in items}
        
    count = 0
    for result_item_id_str, recipe_list in recipes_data.items():
        result_item_id = int(result_item_id_str)
        if result_item_id not in item_id_to_uri:
            continue
            
        result_uri = item_id_to_uri[result_item_id]
        
        for idx, recipe in enumerate(recipe_list):
            count += 1
            recipe_uri = MC[f"recipe_{result_item_id}_{idx}"]
            g.add((recipe_uri, MC.produces, result_uri))
            
            output_quantity = recipe.get('result', {}).get('count', 1)
            g.add((recipe_uri, MC.outputQuantity, Literal(output_quantity, datatype=XSD.integer)))
            
            # --- SHAPED RECIPES (Grid Position) ---
            if 'inShape' in recipe:
                g.add((recipe_uri, RDF.type, MC.ShapedRecipe))
                
                # Iterate through rows and columns
                for row_idx, row in enumerate(recipe['inShape']):
                    for col_idx, item_id in enumerate(row):
                        if item_id is not None and item_id in item_id_to_uri:
                            item_uri = item_id_to_uri[item_id]
                            
                            # 1. Maintain the direct link for easy querying (optional but recommended)
                            g.add((recipe_uri, MC.hasIngredient, item_uri))
                            
                            # 2. Create the specific Slot node for positional data
                            slot_uri = MC[f"recipe_{result_item_id}_{idx}_slot_{row_idx}_{col_idx}"]
                            g.add((slot_uri, RDF.type, MC.RecipeSlot))
                            g.add((slot_uri, MC.slotRow, Literal(row_idx, datatype=XSD.integer)))
                            g.add((slot_uri, MC.slotColumn, Literal(col_idx, datatype=XSD.integer)))
                            g.add((slot_uri, MC.slotItem, item_uri))
                            
                            # 3. Link the recipe to the slot
                            g.add((recipe_uri, MC.hasSlot, slot_uri))

            # --- SHAPELESS RECIPES ---
            elif 'ingredients' in recipe:
                g.add((recipe_uri, RDF.type, MC.ShapelessRecipe))
                for item_id in recipe['ingredients']:
                    if item_id is not None and item_id in item_id_to_uri:
                        g.add((recipe_uri, MC.hasIngredient, item_id_to_uri[item_id]))

    os.makedirs('../ontology', exist_ok=True)
    g.serialize('../ontology/data_recipes.ttl', format='turtle')
    print(f"Exported {count} recipes (Shaped and Shapeless).")

if __name__ == "__main__":
    export_recipes()