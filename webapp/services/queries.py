from config import PREFIXES

def get_classes_query():
    return PREFIXES + """
    SELECT DISTINCT ?class
    WHERE {
      ?class a owl:Class .
      FILTER(STRSTARTS(STR(?class), STR(mc:)))
    }
    ORDER BY ?class
    """

def get_instances_of_class_query(class_name: str):
    return PREFIXES + f"""
    SELECT DISTINCT ?instance
    WHERE {{
      ?instance rdf:type ?type .
      ?type rdfs:subClassOf* mc:{class_name} .
      FILTER(STRSTARTS(STR(?instance), STR(mc:)))
      FILTER(?instance != mc:{class_name})
    }}
    ORDER BY ?instance
    """

def get_resource_details_query(resource_name: str):
    return PREFIXES + f"""
    SELECT ?p ?o
    WHERE {{
      mc:{resource_name} ?p ?o .
    }}
    ORDER BY ?p ?o
    """

def get_resource_inverse_query(resource_name: str):
    return PREFIXES + f"""
    SELECT ?s ?p
    WHERE {{
      ?s ?p mc:{resource_name} .
    }}
    ORDER BY ?p ?s
    """

def get_recipe_ingredients_query(item_name: str):
    return PREFIXES + f"""
    SELECT ?recipe ?ingredient
    WHERE {{
      ?recipe mc:produces mc:{item_name} .
      ?recipe mc:hasIngredient ?ingredient .
    }}
    ORDER BY ?recipe ?ingredient
    """

def get_mobs_that_drop_item_query(item_name: str):
    return PREFIXES + f"""
    SELECT DISTINCT ?mob
    WHERE {{
      {{
        mc:{item_name} mc:droppedBy ?mob .
      }}
      UNION
      {{
        ?mob mc:drops mc:{item_name} .
      }}
    }}
    ORDER BY ?mob
    """

def get_biomes_for_mob_query(mob_name: str):
    return PREFIXES + f"""
    SELECT DISTINCT ?biome
    WHERE {{
      {{
        mc:{mob_name} mc:spawnsIn ?biome .
      }}
      UNION
      {{
        ?biome mc:hasSpawn mc:{mob_name} .
      }}
    }}
    ORDER BY ?biome
    """

def get_tool_for_block_query(block_name: str):
    return PREFIXES + f"""
    SELECT ?tool ?tier
    WHERE {{
      mc:{block_name} mc:minedWith ?tool .
      OPTIONAL {{ mc:{block_name} mc:requiresMinTier ?tier . }}
    }}
    ORDER BY ?tool
    """

def get_items_for_enchantment_query(enchantment_name: str):
    return PREFIXES + f"""
    SELECT ?item
    WHERE {{
      ?item mc:canBeEnchantedWith mc:{enchantment_name} .
    }}
    ORDER BY ?item
    """