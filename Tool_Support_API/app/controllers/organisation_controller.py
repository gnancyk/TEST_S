from flask import Blueprint, request, jsonify
from ..services.organisation_service import get_all_organisations, get_organisation_by_id, check_user_in_ad, check_crm_availability, check_crm_function_general, check_sql_server_availability, get_windows_services, get_sql_catalogs, get_sql_triggers, get_sql_organisation_id, get_sql_ps_functions

bp = Blueprint('organisation', __name__, url_prefix='/organisation')

@bp.route('/organisations', methods=['GET'])
def get_organisations():
    """Récupère toutes les organisations"""
    try:
        organisations = get_all_organisations()
        return jsonify({'status': 200, 'message': 'Organisations récupérées', 'response': organisations})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la récupération des organisations: {str(e)}', 'response': []})

@bp.route('/organisation/<int:id>', methods=['GET'])
def get_organisation(id):
    """Récupère une organisation par ID avec ses paramètres"""
    try:
        organisation = get_organisation_by_id(id)
        if organisation:
            return jsonify({'status': 200, 'message': f'Organisation {id} récupérée', 'response': organisation})
        else:
            return jsonify({'status': 404, 'message': f'Organisation {id} non trouvée', 'response': {}})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la récupération de l\'organisation: {str(e)}', 'response': {}})

@bp.route('/organisation/<int:id>/verification/serveur', methods=['GET'])
def check_organisation_servers(id):
    """Vérifie les serveurs d'une organisation"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')

        if not username or not password:
            return jsonify({'status': 400, 'message': 'Username et password requis', 'response': []})

        result = get_organisation_by_id(id)
        if not result:
            return jsonify({'status': 404, 'message': f'Organisation {id} non trouvée', 'response': []})

        # Logique de vérification des serveurs (à implémenter dans le service)
        servers_status = []  # TODO: Implémenter la logique

        return jsonify({'status': 200, 'message': f'Vérification des serveurs de l\'organisation {id}', 'response': servers_status})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la vérification des serveurs: {str(e)}', 'response': []})

@bp.route('/compte-utilisateur', methods=['GET'])
def check_ad_user():
    """Vérifie si un utilisateur existe dans Active Directory"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')

        if not username or not password:
            return jsonify({'status': 400, 'message': 'Username et password requis', 'response': False})

        result = check_user_in_ad(username, password)
        return jsonify({'status': 200, 'message': 'Vérification AD effectuée', 'response': result})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la vérification AD: {str(e)}', 'response': False})

@bp.route('/disponibilite/frontend-crm', methods=['GET'])
def check_frontend_crm():
    """Vérifie la disponibilité du frontend CRM"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        crm_url = request.args.get('crm_url')
        domaine = request.args.get('domaine', 'univers')

        if not all([username, password, crm_url]):
            return jsonify({'status': 400, 'message': 'Username, password et crm_url requis', 'response': False})

        result = check_crm_availability(crm_url, domaine, username, password)
        return jsonify({'status': 200, 'message': 'Vérification CRM effectuée', 'response': result})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la vérification CRM: {str(e)}', 'response': False})

@bp.route('/disponibilite/crm/fonction_generale', methods=['GET'])
def check_crm_general_function():
    """Vérifie la fonction générale du CRM"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        instance_sql = request.args.get('instance_sql')
        database = request.args.get('database')
        lien_crm = request.args.get('lien_crm')
        serveur_batch = request.args.get('serveur_batch')

        if not all([username, password, instance_sql, database, lien_crm, serveur_batch]):
            return jsonify({'status': 400, 'message': 'Tous les paramètres sont requis', 'response': {}})

        result = check_crm_function_general(instance_sql, database, username, password, lien_crm, serveur_batch)
        return jsonify({'status': result.get('status', 200), 'message': result.get('message', ''), 'response': result})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la vérification de la fonction générale: {str(e)}', 'response': {}})

@bp.route('/disponibilite/serveur-sql', methods=['GET'])
def check_sql_server():
    """Vérifie la disponibilité du serveur SQL"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        instance_sql = request.args.get('instance_sql')

        if not all([username, password, instance_sql]):
            return jsonify({'status': 400, 'message': 'Username, password et instance_sql requis', 'response': False})

        result, version = check_sql_server_availability(instance_sql, username, password)
        return jsonify({'status': 200, 'message': f'Statut du serveur SQL {instance_sql}', 'response': result, 'version': version})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la vérification SQL Server: {str(e)}', 'response': False, 'version': 'N/A'})

@bp.route('/recuperation/service/windows', methods=['GET'])
def get_windows_services():
    """Récupère les services Windows"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        server = request.args.get('server')
        role = request.args.get('role')

        if not all([username, password, server, role]):
            return jsonify({'status': 400, 'message': 'Tous les paramètres sont requis', 'response': []})

        result = get_windows_services(server, role, username, password)
        return jsonify({'status': 200, 'message': f'Services Windows récupérés pour {server}', 'response': result})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la récupération des services: {str(e)}', 'response': []})

@bp.route('/disponibilite/serveur-sql/recuperation/catalogue', methods=['GET'])
def get_catalogs():
    """Récupère les catalogues SQL Server"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        instance_sql = request.args.get('instance_sql')

        if not all([username, password, instance_sql]):
            return jsonify({'status': 400, 'message': 'Username, password et instance_sql requis', 'response': []})

        result = get_sql_catalogs(instance_sql, username, password)
        return jsonify({'status': 200, 'message': f'Catalogues récupérés pour {instance_sql}', 'response': result})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la récupération des catalogues: {str(e)}', 'response': []})

@bp.route('/disponibilite/serveur-sql/recuperation/triggers', methods=['GET'])
def get_triggers():
    """Récupère les triggers SQL Server"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        instance_sql = request.args.get('instance_sql')
        database = request.args.get('database')

        if not all([username, password, instance_sql, database]):
            return jsonify({'status': 400, 'message': 'Tous les paramètres sont requis', 'response': []})

        result = get_sql_triggers(instance_sql, database, username, password)
        return jsonify({'status': 200, 'message': f'Triggers récupérés pour {instance_sql}/{database}', 'response': result})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la récupération des triggers: {str(e)}', 'response': []})

@bp.route('/disponibilite/serveur-sql/recuperation/organisation-id', methods=['GET'])
def get_organisation_id():
    """Vérifie les tables avec OrganizationId"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        instance_sql = request.args.get('instance_sql')
        database = request.args.get('database')

        if not all([username, password, instance_sql, database]):
            return jsonify({'status': 400, 'message': 'Tous les paramètres sont requis', 'response': []})

        result = get_sql_organisation_id(instance_sql, database, username, password)
        return jsonify({'status': 200, 'message': f'Vérification OrganizationId pour {instance_sql}/{database}', 'response': result})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la vérification OrganizationId: {str(e)}', 'response': []})

@bp.route('/disponibilite/serveur-sql/recuperation/ps-functions', methods=['GET'])
def get_ps_functions():
    """Récupère les procédures et fonctions SQL"""
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        instance_sql = request.args.get('instance_sql')
        database = request.args.get('database')

        if not all([username, password, instance_sql, database]):
            return jsonify({'status': 400, 'message': 'Tous les paramètres sont requis', 'response': {}})

        result = get_sql_ps_functions(instance_sql, database, username, password)
        return jsonify({'status': 200, 'message': f'Procédures et fonctions récupérées pour {instance_sql}/{database}', 'response': result})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur lors de la récupération des procédures/fonctions: {str(e)}', 'response': {}})