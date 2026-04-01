from flask import Blueprint, request, jsonify
from ..services.database_service import avoir_version, executer_sql_instance, get_sql_server_catalogs, liste_catalogues, verification_catalogues_ps_function, entite_avec_organisation_id, verification_organisationId

bp = Blueprint('database', __name__, url_prefix='/database')

@bp.route('/disponibilite', methods=['POST'])
def disponibite_et_version():
    try:
        data = request.get_json()
        if not data or 'liste_servers' not in data or 'username' not in data or 'password' not in data:
            return jsonify({'status': 400, 'message': 'Données invalides ou manquantes (liste_servers, username, password)'}), 400
        
        serveurs = data['liste_servers']
        username = data['username']
        password = data['password']
        
        if not isinstance(serveurs, list):
            return jsonify({'status': 400, 'message': 'liste_servers doit être une liste de noms de serveurs'}), 400
        
        versions = {}
        
        for serv in serveurs:
            try:
                version = avoir_version(serv, username, password)
                if version and len(version) > 0:
                    versions[serv] = version[0][0]
                else:
                    versions[serv] = 'Version non récupérée'
            except Exception as e:
                versions[serv] = f'Erreur: {str(e)}'
        
        return jsonify({'status': 200, 'message': 'Versions des serveurs SQL récupérées', 'response': versions})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur interne: {str(e)}'}), 500


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

@bp.route('/recuperation/triggers', methods=['POST'])
def get_triggers():
    data = request.get_json()

    serveurs = data.get('liste_servers')
    username = data.get('username')
    password = data.get('password')
    database = data.get('database')

    statistiques = {}

    for instance in data['liste_servers']['liste']:
        triggers = verifier_trigger(instance['instance'], username, password, database)

        liste_triggers = []
        for elt in triggers:
            liste_triggers.append({
                'nom': elt[0],
                'status': 'Activé' if not elt[3] else 'Désactivé'
            })

        statistiques[instance['serveur']] = {'triggers': len(liste_triggers), 'liste': liste_triggers}

    return jsonify({'status': 200, 'message': "Récupération des triggers", 'response': statistiques})

