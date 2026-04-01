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
    username = data.get('username')
    password = data.get('password')
    centralParam = data.get('centralParam')
    
    import os
    batch_port = os.getenv('BATCH_PORT', '88')
    services = {}
    
    # Extraire la liste des serveurs de manière robuste (gestion du format {'role': {'liste': [...]}} ou {'liste': [...]})
    serveurs = []
    if 'liste' in data.get('liste_servers', {}):
        serveurs = data['liste_servers']['liste']
    else:
        for role, contenu in data.get('liste_servers', {}).items():
            if isinstance(contenu, dict) and 'liste' in contenu:
                serveurs.extend(contenu['liste'])

    for serv in serveurs:
        server_name = serv['serveur']
        service_windows_serveur = service_windows(server_name, username, password)
        services[server_name] = {"anomalies": []}
        
        if not service_windows_serveur:
            continue

        for service in service_windows_serveur:
            fichier_config = service_windows_serveur[service].get('fichier configuration', '')
            if not fichier_config:
                continue
                
            query = f'Get-Content "{fichier_config}"'
            contenu = execution_powershell_hote_distant(server_name, username, password, query)
            
            try:
                if not contenu or not str(contenu).strip():
                    continue
                
                root = ET.fromstring(str(contenu))
                
                for add in root.findall('.//appSettings/add'):
                    if add.attrib.get('key') == 'CentralisationParamEndPoint':
                        centralisationParamEndPoint = add.attrib['value']
                        parts = centralisationParamEndPoint.split('/')
                        if len(parts) >= 5:
                            serveur_batch_avec_port = parts[2]
                            serveur_batch_recupere = serveur_batch_avec_port.split(':')[0]
                            
                            new_centralparam = f"{parts[0]}//{server_name}:{batch_port}/{parts[3]}/{parts[4]}"
                            
                            is_anomaly = False
                            if serveur_batch_recupere.lower() in [server_name.lower(), 'localhost']:
                                if centralParam and centralParam.lower() != new_centralparam.lower():
                                    is_anomaly = True
                            else:
                                is_anomaly = True
                                
                            if is_anomaly:
                                services[server_name]["anomalies"].append({
                                    "service" : service_windows_serveur[service].get('service', service)
                                })
            except Exception as e:
                # Gérer le cas où le XML n'est pas parsable (ex: fichier inexistant ou corrompu)
                services[server_name]["anomalies"].append({
                    "service" : service_windows_serveur[service].get('service', service),
                    "erreur" : "Fichier de configuration introuvable ou XML malformé"
                })

    return jsonify({'status':200,'message':f"Informations sur les services windows",'response':services})

