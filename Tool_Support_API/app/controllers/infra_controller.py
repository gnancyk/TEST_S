from flask import Blueprint, request, jsonify
from ..services.verification_infra_service import server_disponible, verification_antivirus,recuperation_os_information,performances_serveur

import json


bp = Blueprint('infra', __name__, url_prefix='/infra')

@bp.route('/disponibilite/serveur', methods=['POST'])
def disponibilite_serveur():
    data = request.get_json()
    disponibilites = {}
    
    for role in data['liste_servers']:
        role_serveurs = {}
        for serv in data['liste_servers'][role]['liste']:
            etat_serveur = server_disponible(serv['serveur'])
            role_serveurs[serv['serveur']] = etat_serveur
            # print (serv, etat_serveur)

        disponibilites[role] = role_serveurs
            
    return jsonify({'status':200,'message':f"Disponibilité des serveurs {data}",'response':disponibilites})



@bp.route('/caracteristiques/serveur', methods=['POST'])
def informations_serveur():
    data = request.get_json()
    username = data['username']
    password = data['password']
    caracteristiques = {}
    
    for role in data['liste_servers']:
        role_serveurs = {}
        for serv in data['liste_servers'][role]['liste']:
            caracteristique_serveur = recuperation_os_information(serv['serveur'], username, password)
            role_serveurs[serv['serveur']] = {'OS': caracteristique_serveur[0].strip(), 'Version':caracteristique_serveur[1].strip(),'Dernier demarrage':caracteristique_serveur[2].strip(),'Nombre de processeurs':caracteristique_serveur[3].strip()}
            
        caracteristiques[role] = role_serveurs
        
    return jsonify({'status':200,'message':f"Informations sur les serveurs",'response':caracteristiques})

@bp.route('/performances/serveur', methods=['POST'])
def performances():
    data = request.get_json()
    username = data['username']
    password = data['password']
    caracteristiques = {}
    
    for role in data['liste_servers']:
        role_serveurs = {}
        for serv in data['liste_servers'][role]['liste']:
            # print(serv['serveur'], username,password)
            performances = performances_serveur(serv['serveur'], username, password)
            role_serveurs[serv['serveur']] = performances
            # print(performances)
        caracteristiques[role] = role_serveurs
        
    return jsonify({'status':200,'message':f"Informations sur les performances des serveurs",'response':caracteristiques})



@bp.route('/antivirus', methods=['POST'])
def informations_antivirus():
    data = request.get_json()
    username = data['username']
    password = data['password']
    caracteristiques = {}
    
    # print( data)
    for role in data['liste_servers'] :
        # print (role)
        role_serveurs = {}
        for liste in data['liste_servers'][role]:
            # print(data['liste_servers'][role][liste])
            for serveur in  data['liste_servers'][role][liste]:
                if  isinstance(serveur, dict) : 
                    av_serveurs = { }
                    # print(serveur['serveur'])
                    liste_antivirus = verification_antivirus(serveur['serveur'], username, password)
                    if liste_antivirus:
                        antivirus = json.loads(liste_antivirus)
                        # print(antivirus)
                        if isinstance(antivirus, list):
                            # Parcourir une liste de dictionnaires
                            for av in antivirus:
                                # print(av)
                                av_serveurs[av['DisplayName']] =  av['Status']
                                
                        elif isinstance(antivirus, dict):
                            # print(antivirus)
                            av_serveurs[antivirus['DisplayName']] =  antivirus['Status']
                        
                        role_serveurs[serveur['serveur']]=av_serveurs
        
        caracteristiques[role] = role_serveurs
            # for serveur in liste:
            #     print(serveur['serveur'])
    return jsonify({'status':200,'message':f"Informations sur les antivirus",'response':caracteristiques})
    