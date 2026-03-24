import requests
from urllib.parse import urlparse
from zeep import Client
import subprocess
import wmi
import json
import os
from pathlib import Path
import winrm
import xml.etree.ElementTree as ET

def verifier_lien(url):
    parsed_url = urlparse(url)

    if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc:
        print("URL valide")
    else:
        print("URL invalide")
        

def verifier_service_soap(url):
    response = requests.get(url)

    if response.status_code == 200 and 'soap+xml' in response.headers.get('Content-Type', ''):
        print("C'est un service SOAP")
    else:
        print("Ce n'est pas un service SOAP")
        
def check_svc_service(url):
    try:
        # Envoi d'une requête GET pour tester l'accès au service
        response = requests.get(url)
        
        # Vérifie si la réponse est OK (status code 200)
        if response.status_code == 200:
            # Vérifie si la réponse contient quelque chose d'attendu pour un service SVC
            if "Service" in response.text or "WCF" in response.text:
                print("C'est un service SVC.")
                return True
            else:
                print("Réponse non spécifique au service SVC.")
                return False
        else:
            print(f"Échec de la connexion au service SVC, code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return False




def avoir_configuration_central_param(url):
    ext_param = '?wsdl'
    wsdl = url + ext_param  # ou ton vrai chemin
    client = Client(wsdl=wsdl)

    print("=== Services disponibles ===")
    for service in client.wsdl.services.values():
        service_name = service.name
        print(f"Service: {service.name}")
        for port in service.ports.values():
            print(f"  Port: {port.name}")
            service_port = port.name
            operations = port.binding._operations
            print("  Opérations disponibles:")
            for operation in operations:
                print(f"    - {operation}")
    print( service_name, service_port)
    return service_name, service_port

def execution_powershell_hote_distant(server, username, password,query):
    # Créer une chaîne d'informations d'identification PowerShell
    
    creds_command = f"$username = '{username}'; $password = ConvertTo-SecureString '{password}' -AsPlainText -Force; $cred = New-Object System.Management.Automation.PSCredential($username, $password)"
    
    
    ps_command = f"""
    $session = New-PSSession -ComputerName {server} -Credential $cred;
    Invoke-Command -Session $session -ScriptBlock {{ {query} }};
    Remove-PSSession -Session $session
    """

    # Exécuter la commande PowerShell avec la connexion distante
    result = subprocess.run(
        ["powershell", "-Command", creds_command + ps_command],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        output = result.stdout.strip()
        # output = result.std_out.decode('utf-8').strip()

        
        return output
    else:
        return ''




# def get_remote_antivirus_info(host, user, password):
#     try:
#         connection = wmi.WMI(
#             computer=host,
#             user=user,
#             password=password,
#             namespace="root\\SecurityCenter2"
#         )
#         antivirus_products = connection.AntiVirusProduct()
#     except Exception as e:
#         return f"Erreur de connexion ou de récupération WMI : {e}"

#     if not antivirus_products:
#         return "Aucun antivirus détecté sur la machine distante."

#     result = []
#     for av in antivirus_products:
#         result.append({
#             "Nom": av.displayName,
#             "Etat": av.productState,
#             "Chemin": av.pathToSignedProductExe
#         })
#     return result



remote_host = "gsecrms1t"
remote_user = "univers\\adminsaphirv3"
remote_password = "Operating0"

# antivirus = get_remote_antivirus_info(remote_host, remote_user, remote_password)

# if isinstance(antivirus, str):
#     print(antivirus)
# else:
#     for av in antivirus:
#         print(f"Nom : {av['Nom']}")
#         print(f"État : {av['Etat']}")
#         print(f"Chemin : {av['Chemin']}")
#         print("-" * 30)


def get_remote_info(server, username, password):
    conn = wmi.WMI(
        computer=server,
        user=username,
        password=password
    )

    # Disques
    drives = [{
        'DeviceID': d.DeviceID,
        'Size(GB)': round(int(d.Size) / (1024 ** 3), 2) if d.Size else None,
        'FreeSpace(GB)': round(int(d.FreeSpace) / (1024 ** 3), 2) if d.FreeSpace else None
    } for d in conn.Win32_LogicalDisk(DriveType=3)]

    # RAM
    os = conn.Win32_OperatingSystem()[0]
    ram = {
        'TotalRAM(GB)': round(int(os.TotalVisibleMemorySize) / (1024 ** 2), 2),
        'FreeRAM(GB)': round(int(os.FreePhysicalMemory) / (1024 ** 2), 2)
    }

    # CPU Info
    cpu_info = [{
        'Name': c.Name,
        'Cores': c.NumberOfCores,
        'LogicalProcessors': c.NumberOfLogicalProcessors,
        'MaxClockSpeed': c.MaxClockSpeed
    } for c in conn.Win32_Processor()]

    return {
        'Server': server,
        'Drives': drives,
        'RAM': ram,
        'CPU': cpu_info
    }



# ext = '?wsdl'
# url = 'http://GSESPHV3B8PP:88/CIE_CentralisationParam/CentralisationParam.svc'
# # url2 = 'http://gsecrmc1t:5555/CIETIF/main.aspx#496802547'

# # verifier_lien(url + ext)
# # # verifier_service_soap(url)
# # check_svc_service(url)
# # # avoir_configuration_central_param(url)

# # text = 'cie.ci;sodeci.ci;gs2e.ci;gs2e.ci;sde.sn;'
# # [print(elt)  for elt in text.split(';') if elt != '']

# query = """
#                 Get-Service | Where-Object { $_.DisplayName -like "*McAfee*" -or $_.DisplayName -like "*Windows Defender*" -or $_.DisplayName -like "*Kaspersky Endpoint*" }   | Select-Object Status,DisplayName,PSComputerName | ConvertTo-Json
#             """
            
#                 # Get-Service | Where-Object { $_.DisplayName -like "*McAfee*" -or $_.DisplayName -like "*Windows Defender*" -or $_.DisplayName -like "*Kaspersky Endpoint*" }  | Select-Object Status,DisplayName,PSComputerName
# # antivirus = execution_powershell_hote_distant("gsecrmc1t", "adminsaphirv3", "Operating0",query)
# antivirus1 = execution_powershell_hote_distant("gsecrms1t", "adminsaphirv3", "Operating0",query)
# antivirus2 = execution_powershell_hote_distant("gsecrmb1t", "adminsaphirv3", "Operating0",query)



# print(antivirus1)
# print(json.loads(antivirus1))
# # print ( antivirus1)
# # antivirus[antivirus.find('------   ----               -----------                            --------------')]

# resultats_pre1 = antivirus1.split('------   ----               -----------                            --------------') 
# resultats_pre2 = antivirus1.split('PSComputerName')
# # resultats_pre = resultats_pre1[1].split('gsecrms1t') 

# # print(antivirus1)
# # print(resultats_pre2)

# for av in json.loads(antivirus1):
#   # status = av[av.find("Status         : ") + len("Status         : "):av.find("DisplayName    :")]  
#   print(av['Status'])


# # for av in antivirus1:
# #   print(av)
# # print(resultats_pre2)
# # for av in resultats_pre:
# #   print(av)
# # print(resultats_pre)




# # Exemple d'appel
server = 'gsecrmb1t'
username = 'univers\\adminsaphirv3'
password = 'Operating0'

# info = get_remote_info(server, username, password)
# print(info)



# Connexion distante WMI
connection = wmi.WMI(
    computer=server,
    user=username,
    password=password
)
fs = connection.CIM_DataFile  # Pour interroger les fichiers

config_extensions = [".ini", ".config", ".xml", ".json"]

# Filtrer les services contenant 'DEMO'
for service in connection.Win32_Service():
    if 'SAPHIRV3' in service.Name.upper() or \
       'SAPHIRV3' in (service.DisplayName or '').upper() or \
       'SAPHIRV3' in (service.Description or '').upper():
        print(f"Name:             {service.Name}")
        print(f"Display Name:     {service.DisplayName}")
        print(f"Description:      {service.Description}")
        print(f"PathName:         {service.PathName}")
        print(f"Start Mode:       {service.StartMode}")
        print(f"State:            {service.State}")
        print(f"Status:           {service.Status}")
        print(f"Start Name:       {service.StartName}")
        print(f"Executable Path: {service.PathName}")
        # print(f"Service Type:     {service.ServiceType}")
        # print(f"Error Control:    {service.ErrorControl}")
        # print(f"Accept Pause:     {service.AcceptPause}")
        # print(f"Accept Stop:      {service.AcceptStop}")
        # print(f"Desktop Interact: {service.DesktopInteract}")
        # print(f"Dependencies:     {service.Dependencies}")
        
        print(service)
        # Extraire le chemin de l'exécutable (sans guillemets ni arguments)
        exe_path = service.PathName.strip('"').split(' ')[0]

        # Récupérer la version du fichier exécutable
        try:
            exe_info = fs(Name=exe_path)
            if exe_info:
                version = exe_info[0].Version
                print(f"Version:     {version}")
            else:
                print("Version:     Non trouvée")
        except Exception as e:
            print(f"Erreur WMI pour version: {e}")
            
        exe_path = service.PathName.strip('"').split(' ')[0]

        # Récupérer le dossier du service (là où l'exécutable est situé)
        folder = str(Path(exe_path).parent)

        print(f"Recherche de fichiers de configuration dans: {folder}")

        exe_path = service.pathname.strip('"')  
        
        print(exe_path + ".config")
        # Lister les fichiers dans ce dossier
        try:
            config_files = [f for f in os.listdir(folder) if any(f.lower().endswith(ext) for ext in config_extensions)]
            
            # if config_files:
            #     for config_file in config_files:
            #         print(f"  -> Fichier de config trouvé: {config_file}")
            #         # Si le fichier est XML, on peut le lire
            #         if config_file.lower().endswith('.xml'):
            #             config_file_path = os.path.join(folder, config_file)
            #             try:
            #                 # Lire et parser le fichier XML
            #                 tree = ET.parse(config_file_path)
            #                 root = tree.getroot()
            #                 print(f"Contenu de {config_file}:")
            #                 for elem in root.iter():
            #                     print(f"{elem.tag} = {elem.text}")
            #             except Exception as e:
            #                 print(f"Erreur lors de la lecture du fichier XML: {e}")
            # else:
            #     print("  Aucun fichier de configuration trouvé.")
            # exe_path = service.PathName.strip('"').split(' ')[0]

            # Récupérer le dossier du service (là où l'exécutable est situé)
            # folder = str(Path(exe_path))
            # print(folder)
            # print(str(service.PathName + '.config'))
            # # Concaténer le nom du fichier .config au chemin de l'exécutable
            # config_file_path = os.path.join(folder, f"{service.Name}.config")

            # print(config_file_path)
            
            
            # chemin = Path(service.PathName)
            # config_chemin = chemin.with_suffix(chemin.suffix + ".config")
            # print(config_chemin)
            
           # The above code is written in Python and it checks if a file specified by the variable
           # `config_chemin` exists. If the file exists, it parses the XML content of the file using
           # ElementTree, prints the content of the XML elements, and then reads and prints the entire
           # content of the file. If the file does not exist, it simply prints "Fichier de
           # configuration non trouvé." which means "Configuration file not found" in French.
           
            # if os.path.exists(config_chemin):
            #     tree = ET.parse(config_chemin)
            #     root = tree.getroot()
            #     print(f"Contenu de {config_chemin}:")
            #     for elem in root.iter():
            #         print(f"{elem.tag} = {elem.text}")
            #     print(f"Le fichier de configuration a été trouvé : {config_chemin}")
            #     # Lire le fichier si c'est un fichier texte ou config
            #     with open(config_chemin, 'r') as file:
            #         print(file.read())  # Affiche le contenu du fichier
            # else:
            #     print("Fichier de configuration non trouvé.")
                
            
        except Exception as e:
            print(f"Erreur lors de l'accès au dossier: {e}")
        
        
        
        print("-" * 40)
        
# connection = wmi.WMI(
#     computer=server,
#     user=username,
#     password=password,
#     namespace="root\\WebAdministration"
# )

# # Lister les sites IIS
# for site in connection.query("SELECT * FROM IIsWebServer"):
#     print(f"Site: {site.Name} (State: {site.ServerAutoStart})")
    
#     # Lister les applications liées à ce site
#     for app in connection.query(f"SELECT * FROM IIsWebApplication WHERE ServerBindings = '{site.ServerBindings}'"):
#         print(f"  Application: {app.Name}")
#         print(f"    Physical Path: {app.Path}")
#         print(f"    Alias: {app.Alias}")
#         print(f"    State: {app.ServerAutoStart}")