from flask import Blueprint, request, jsonify
from ..services.database_service import avoir_version, executer_sql_instance, get_sql_server_catalogs, liste_catalogues, verification_catalogues_ps_function, entite_avec_organisation_id, verification_organisationId

bp = Blueprint('database', __name__, url_prefix='/database')

@bp.route('/disponibilite', methods=['POST'])
def disponibite_et_version():
    data = request.get_json()
    
    serveurs = data.get('liste_servers')
    username = data.get('username')
    password = data.get('password')
    
    versions = {}
    
    # print(serveurs)
    
    serveur = {}
    for serv in serveurs:
        version = avoir_version(serv, username, password) 
        # print(serv)
        serveur[serv] = version[0][0]
        # print(serv, version[0])
        
    versions = serveur
        
    return jsonify({'status': 200, 'message': f"Version du serveur SQL récupérée {serveurs}", 'response': versions})


@bp.route('/statistique', methods=['POST'])
def statistique_ps_function():
    data = request.get_json()
    
    serveurs = data.get('liste_servers')
    username = data.get('username')
    password = data.get('password')
    
    statistiques = {}
    
    liste_func = []
    liste_ps   = []
    # print(data)
    for instance in data['liste_servers']['liste']:
        print(instance['instance'])
        procedures = get_sql_server_catalogs(instance['instance'],username,password)
        procedures_list = []
        for proc in procedures:
            procedures_list.append({
                'source':proc.SPECIFIC_CATALOG,
                'nom': proc.ROUTINE_NAME,
                'type': proc.ROUTINE_TYPE,
                # 'definition': proc.ROUTINE_DEFINITION
            })
            if proc.ROUTINE_TYPE == 'FUNCTION':
                liste_func.append(proc)
            else:
                liste_ps.append(proc)
        catalogues = liste_catalogues(instance['instance'],username,password)
        # print(instance['serveur'], len(liste_ps),len(liste_func),len(catalogues))
        statistiques[instance['serveur']] = {'PS':len(liste_ps),'fonctions':len(liste_func),'catalogues': len(catalogues),'liste_ps':liste_ps,'liste_func':liste_func,'liste_catalogues':catalogues}
        statistiques[instance['serveur']] = {'PS':len(liste_ps),'fonctions':len(liste_func),'catalogues': len(catalogues)}
        
    return jsonify({'status': 200, 'message':"Statisitque sur les procedures et fonctions", 'response': statistiques})




@bp.route('/verification/catalogue', methods=['POST'])
def analyse_catalogue():
    data = request.get_json()
    
    serveurs = data.get('liste_servers')
    username = data.get('username')
    password = data.get('password')
    
    statistiques = {}
    
    # print(data)
    for instance in data['liste_servers']['liste']:
        print(instance['instance'])
        recuperation, ps , fn = verification_catalogues_ps_function(instance['instance'],username,password)
        print(len(ps),len(fn))
        
        
        statistiques[instance['serveur']] = {'ps':len(ps),'function':len(fn),'tout':len(recuperation),'liste_ps':ps,'liste_fn':fn,'all':recuperation}
        
    return jsonify({'status': 200, 'message':"Vérification catalogues sur les procedures et fonctions", 'response': statistiques})


@bp.route('/verification/organisation_id', methods=['POST'])
def verification_organisation_id():
    data = request.get_json()
    
    serveurs = data.get('liste_servers')
    username = data.get('username')
    password = data.get('password')
    database = data.get('catalogue_mscrm')
    
    statistiques = {}
    
    # print(data)
    for instance in data['liste_servers']['liste']:
        resultats = entite_avec_organisation_id(instance['instance'], username, password, database)
        entities = [column[0] for column in resultats]
        retour = verification_organisationId(instance['instance'], username, password, database,entities)
                
        statistiques[instance['serveur']] = {'soucis':len(retour),'all':retour}
    
    return jsonify({'status': 200, 'message':"Vérification OrganisationID", 'response': statistiques})

