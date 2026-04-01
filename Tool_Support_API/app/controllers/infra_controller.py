from flask import Blueprint, request, jsonify
from ..services.verification_infra_service import server_disponible, verification_antivirus,recuperation_os_information,performances_serveur

import json


bp = Blueprint('infra', __name__, url_prefix='/infra')

@bp.route('/disponibilite/serveur', methods=['POST'])
def disponibilite_serveur():
    try:
        data = request.get_json()
        if not data or 'liste_servers' not in data:
            return jsonify({'status': 400, 'message': 'Données invalides ou manquantes'}), 400
        
        disponibilites = {}
        
        for role in data['liste_servers']:
            if 'liste' not in data['liste_servers'][role]:
                return jsonify({'status': 400, 'message': f'Structure invalide pour le rôle {role}'}), 400
            role_serveurs = {}
            for serv in data['liste_servers'][role]['liste']:
                if 'serveur' not in serv:
                    return jsonify({'status': 400, 'message': 'Nom de serveur manquant'}), 400
                etat_serveur = server_disponible(serv['serveur'])
                role_serveurs[serv['serveur']] = etat_serveur
            disponibilites[role] = role_serveurs
            
        return jsonify({'status': 200, 'message': f"Disponibilité des serveurs vérifiée", 'response': disponibilites})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur interne: {str(e)}'}), 500



@bp.route('/caracteristiques/serveur', methods=['POST'])
def informations_serveur():
    try:
        data = request.get_json()
        if not data or 'liste_servers' not in data or 'username' not in data or 'password' not in data:
            return jsonify({'status': 400, 'message': 'Données invalides ou manquantes (liste_servers, username, password)'}), 400
        
        username = data['username']
        password = data['password']
        caracteristiques = {}
        
        for role in data['liste_servers']:
            if 'liste' not in data['liste_servers'][role]:
                return jsonify({'status': 400, 'message': f'Structure invalide pour le rôle {role}'}), 400
            role_serveurs = {}
            for serv in data['liste_servers'][role]['liste']:
                if 'serveur' not in serv:
                    return jsonify({'status': 400, 'message': 'Nom de serveur manquant'}), 400
                caracteristique_serveur = recuperation_os_information(serv['serveur'], username, password)
                if caracteristique_serveur == ('N/A', 'N/A', 'N/A', 'N/A'):
                    return jsonify({'status': 500, 'message': f'Impossible de récupérer les informations pour {serv["serveur"]}'}), 500
                role_serveurs[serv['serveur']] = {'OS': caracteristique_serveur[0].strip(), 'Version': caracteristique_serveur[1].strip(),'Dernier demarrage': caracteristique_serveur[2].strip(),'Nombre de processeurs': caracteristique_serveur[3].strip()}
            caracteristiques[role] = role_serveurs
        
        return jsonify({'status': 200, 'message': f"Informations sur les serveurs récupérées", 'response': caracteristiques})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur interne: {str(e)}'}), 500

@bp.route('/performances/serveur', methods=['POST'])
def performances():
    try:
        data = request.get_json()
        if not data or 'liste_servers' not in data or 'username' not in data or 'password' not in data:
            return jsonify({'status': 400, 'message': 'Données invalides ou manquantes (liste_servers, username, password)'}), 400
        
        username = data['username']
        password = data['password']
        performances_data = {}
        
        for role in data['liste_servers']:
            if 'liste' not in data['liste_servers'][role]:
                return jsonify({'status': 400, 'message': f'Structure invalide pour le rôle {role}'}), 400
            role_serveurs = {}
            for serv in data['liste_servers'][role]['liste']:
                if 'serveur' not in serv:
                    return jsonify({'status': 400, 'message': 'Nom de serveur manquant'}), 400
                perf = performances_serveur(serv['serveur'], username, password)
                if not perf or 'Server' not in perf:
                    return jsonify({'status': 500, 'message': f'Impossible de récupérer les performances pour {serv["serveur"]}'}), 500
                role_serveurs[serv['serveur']] = perf
            performances_data[role] = role_serveurs
        
        return jsonify({'status': 200, 'message': f"Informations sur les performances des serveurs récupérées", 'response': performances_data})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur interne: {str(e)}'}), 500



@bp.route('/antivirus', methods=['POST'])
def informations_antivirus():
    try:
        data = request.get_json()
        if not data or 'liste_servers' not in data or 'username' not in data or 'password' not in data:
            return jsonify({'status': 400, 'message': 'Données invalides ou manquantes (liste_servers, username, password)'}), 400
        
        username = data['username']
        password = data['password']
        caracteristiques = {}
        
        for role in data['liste_servers']:
            if 'liste' not in data['liste_servers'][role]:
                return jsonify({'status': 400, 'message': f'Structure invalide pour le rôle {role}'}), 400
            role_serveurs = {}
            for serv in data['liste_servers'][role]['liste']:
                if 'serveur' not in serv:
                    return jsonify({'status': 400, 'message': 'Nom de serveur manquant'}), 400
                av_serveurs = {}
                liste_antivirus = verification_antivirus(serv['serveur'], username, password)
                if liste_antivirus:
                    try:
                        antivirus = json.loads(liste_antivirus)
                        if isinstance(antivirus, list):
                            for av in antivirus:
                                av_serveurs[av['DisplayName']] = av['Status']
                        elif isinstance(antivirus, dict):
                            av_serveurs[antivirus['DisplayName']] = antivirus['Status']
                    except json.JSONDecodeError:
                        return jsonify({'status': 500, 'message': f'Erreur de parsing JSON pour {serv["serveur"]}'}), 500
                role_serveurs[serv['serveur']] = av_serveurs
            caracteristiques[role] = role_serveurs
        
        return jsonify({'status': 200, 'message': f"Informations sur les antivirus récupérées", 'response': caracteristiques})
    except Exception as e:
        return jsonify({'status': 500, 'message': f'Erreur interne: {str(e)}'}), 500
    