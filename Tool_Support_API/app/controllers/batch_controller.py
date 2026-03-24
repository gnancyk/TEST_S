from flask import Blueprint, request, jsonify
from ..services.verification_serveur_service import service_windows
from ..utils.powershell_scripting import execution_powershell_hote_distant
import xml.etree.ElementTree as ET


bp = Blueprint('batch', __name__, url_prefix='/batch')


@bp.route('/services/windows', methods=['POST'])
def liste_service_windows():
    data = request.get_json()
    username = data['username']
    password = data['password']
    services = {}
    # print(data)
    for role in data['liste_servers']:
        role_serveurs = {}
        for serv in data['liste_servers']['liste']:
            service_windows_serveur = service_windows(serv['serveur'], username, password)
            role_serveurs[serv['serveur']] = service_windows_serveur
        
        services[role] = role_serveurs
        
    return jsonify({'status':200,'message':f"Informations sur les services windows",'response':services})



@bp.route('/services/windows/verification/config', methods=['POST'])
def verification_config_service_windows():
    data = request.get_json()
    username = data['username']
    password = data['password']
    centralParam = data['centralParam']
    services = {}
    # print(data)
    # for role in data['liste_servers']:
    role_serveurs = {}
    for serv in data['liste_servers']['liste']:
        service_windows_serveur = service_windows(serv['serveur'], username, password)
        # print(service_windows_serveur)
        for service in service_windows_serveur:
            
            fichier_config = service_windows_serveur[service]['fichier configuration']
            query = f"""
                Get-Content "{fichier_config}" 
            """
            contenu = execution_powershell_hote_distant(serv['serveur'], username, password,query)
            # print(contenu)
            serveur_batch_fournir = serv['serveur']
           
            root = ET.fromstring(contenu)
           
            
            for add in root.findall('appSettings'):
                for add1 in add.findall('add'):
                    # print(add1.attrib.get('key') )
                    if add1.attrib.get('key') == 'CentralisationParamEndPoint':
                        centralisationParamEndPoint = add1.attrib['value']
                        serveur_batch_avec_port = centralisationParamEndPoint.split('/')[2]
                        serveur_batch_recupere = serveur_batch_avec_port.split(':')[0]
                        
                        new_centralparam= centralisationParamEndPoint.split('/')[0]+f'//{serveur_batch_fournir}:88'+'/'+centralisationParamEndPoint.split('/')[3]+'/'+centralisationParamEndPoint.split('/')[4]
                        # print("Valeur trouvée :", add1.attrib['value'].lower())
                        # print("Valeur modifiée :", new_centralparam.lower())
                        
                        if serveur_batch_recupere.lower() == serveur_batch_fournir.lower() or serveur_batch_recupere.lower() == 'localhost':
                            # if add1.attrib['value'].lower() != new_centralparam.lower():
                            if centralParam.lower() != new_centralparam.lower():
                                print('souci \n')
                                print(add1.attrib['value'].lower())
                                print(new_centralparam.lower())
                                role_serveurs[serv['serveur']] = {
                                    "service" : service_windows_serveur[service]['service'] 
                                }
                                print(role_serveurs)
                        
                        else:
                            role_serveurs[serv['serveur']] = {
                                    "service" : service_windows_serveur[service]['service'] 
                                }
                            
                            print(role_serveurs)
                        
                        
                            
    
    print(role_serveurs)
        
    services[serv['serveur']] = role_serveurs
        
    return jsonify({'status':200,'message':f"Informations sur les services windows",'response':services})
