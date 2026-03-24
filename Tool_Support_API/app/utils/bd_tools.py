import re

def analyser_catalogues(proc_definition):
    # Rechercher les occurrences de catalogues (ex : database.schema.table)
    catalogues_utilises = set()
    # catalogues_utilises = []
    
    # Chercher des patterns de catalogues typiques : base.schema.table
    # Cela peut varier en fonction de la convention utilisée dans ta base de données

    pattern = r'([a-zA-Z0-9_]+)\.([a-zA-Z]+)\.([a-zA-Z0-9_]+)'
    # pattern = r'([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)'
    matches = re.findall(pattern, proc_definition)
    
    for match in matches:
        base, schema, table = match
        # catalogues_utilises.add(f'{base}.{schema}')
        # catalogues_utilises.add({'base':f'{base}', 'table':table, 'schema':schema})
        catalogues_utilises.add(f'{base}')
    
    return catalogues_utilises
