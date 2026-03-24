import subprocess
from ..utils.extraction_texte import extracteur
from ..utils.powershell_scripting import execution_powershell_hote_distant
import wmi
import pythoncom
import json
    
def recuperation_status_service_windows(server, username, password,query):
    reponse_service_distance = execution_powershell_hote_distant(server, username, password,query)
    
    if reponse_service_distance != '':
        # statut = reponse_service_distance[reponse_service_distance.find("------  -------------- ----------") + len("------  -------------- ----------"):reponse_service_distance.find(server)] 
        statut = extracteur(reponse_service_distance,"------  -------------- ----------",server) 
        return statut
    else:
        return 'N/A'


def service_windows(server, username, password):
    pythoncom.CoInitialize()

    try:
        connection = wmi.WMI(
            computer=server,
            user=username,
            password=password
        )
        services = {}
        for service in connection.Win32_Service():
            if 'SAPHIRV3' in service.Name.upper() or \
            'SAPHIRV3' in (service.DisplayName or '').upper() or \
            'SAPHIRV3' in (service.Description or '').upper():
                
                # Convertit les propriétés de l'objet en dictionnaire
                service_dict = {prop: getattr(service, prop) for prop in service.properties.keys()}

                # Convertit en JSON
                service_json = json.dumps(service_dict, indent=4)
                
                # print(service_json)
                exe_path = service.pathname.strip('"')  
                fichier_config = exe_path + ".config"
                services[service.Name] = {
                    "service":  json.loads(service_json),
                    "fichier configuration": fichier_config
                }
        return services
    
    finally:
        pythoncom.CoUninitialize()

    