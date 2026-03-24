# import requests
# from requests_ntlm import HttpNtlmAuth
# import winrm
# import subprocess

from zeep import Client

wsdl = 'http://gsecrmb1t:88/CIETIF_CentralisationParam/CentralisationParam.svc?wsdl'  # ou ton vrai chemin
client = Client(wsdl=wsdl)

# Voir tous les services, ports et opérations disponibles
from zeep import helpers




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
            



# Remplace par ton vrai lien

# 2. Création du client et liaison au bon service/port
client = Client(wsdl=wsdl)
service = client.bind(service_name,service_port)
# service = client.bind('CentralisationParam', 'BasicHttpBinding_ICentralisationParam')

# 3. Récupération des types
ArrayOfParameter = client.get_type('ns2:ArrayOfParameter')
Parameter = client.get_type('ns2:Parameter')

# 4. Construction de la liste des paramètres
params_list = [
    # Parameter(ParamName='CrmConnectionString'),  # Adapte les noms si besoin
    # Parameter(Name='Type', Value='X')
]

# 5. Création de l'objet attendu par le service
array_of_params = ArrayOfParameter(params_list)

# 6. Appel de la méthode SOAP avec le bon paramètre
response = service.GetParameter(_prameters=array_of_params)

# 7. Affichage du résultat
print("=== Résultat reçu du service ===")
# print(response)
# print(type(response))
print(response.ListOfParmeters.Parameter[0])


# filtré = [d for d in response if d['ParamName'].startswith('Working')]

            


##################################################
# Trigger information
#####  
# SELECT 
#     name,
#     parent_id,
#     type_desc,
#     is_disabled
# FROM 
#     sys.triggers
######



# import requests
# from requests.auth import HTTPBasicAuth
# import xml.etree.ElementTree as ET

# Paramètres de connexion à Dynamics CRM
crm_url ="http://gsecrmc1t:5555/CIETIF/XRMServices/2011/Organization.svc"
username = "adminsaphirv3"
password = "Operating0"
domain = "univers"

# # Fonction pour effectuer une requête SOAP et obtenir les informations sur le chiffrement
# def check_encryption_key():
#     # Corps de la requête SOAP pour interroger les paramètres du serveur CRM
#     soap_request = """
#     <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
#                 xmlns:a="http://schemas.microsoft.com/xrm/2011/Contracts/Services">
#         <s:Body>
#             <a:RetrieveOrganizationRequest />
#         </s:Body>
#     </s:Envelope>
#     """

#     headers = {
#         'Content-Type': 'text/xml; charset=utf-8',
#         'Accept': 'application/soap+xml, application/xml',
#     }

#     # Effectuer la requête HTTP POST pour appeler l'API SOAP de CRM
#     response = requests.post(crm_url, data=soap_request, headers=headers, auth=HTTPBasicAuth(f'{domain}\\{username}', password))

#     if response.status_code == 200:
#         # Parse la réponse XML
#         tree = ET.ElementTree(ET.fromstring(response.content))
#         root = tree.getroot()

#         # Rechercher l'élément indiquant la clé de chiffrement
#         # Exemple basé sur les données retournées, adapte en fonction de la structure de la réponse réelle
#         for elem in root.iter():
#             if 'EncryptionKey' in elem.tag:
#                 print("La clé de chiffrement est renseignée.")
#                 return
#         print("La clé de chiffrement n'est pas renseignée.")
#     else:
#         print(f"Erreur lors de la requête : {response.status_code}, {response.text}")

# # Exécuter la vérification
# check_encryption_key()


















###############################################################################################""
#
#                      VERIFICATION DE LA VERSION DE CRM
#
###############################################################################################
# # Configuration de ton environnement
# crm_url = "http://ddisphv3c2t/SODECITIF"
# # crm_url = "http://gsecrmc1t:5555/CIETIF"
# web_api_url = f"{crm_url}/api/data/v8.0/"

# # Identifiants Windows (NTLM)
# # username = "Univers\\adminsaphirv3"
# # password = "Operating0"
# username = "Univers\\AdminSaphirV3PP"
# password = "$pecial@ccountpp02"

# # Authentification NTLM
# auth = HttpNtlmAuth(username, password)

# # Appel Web API
# headers = {
#     'OData-MaxVersion': '4.0',
#     'OData-Version': '4.0',
#     'Accept': 'application/json',
#     'Content-Type': 'application/json'
# }

# # Test de connexion à l'API
# response = requests.get(web_api_url, headers=headers, auth=auth, verify=False)  # verify=False si tu as un certif self-signed

# if response.status_code == 200:
#     print("Connexion à l'API OK")
    
#     # Appel de la fonction RetrieveVersion
#     version_url = f"{web_api_url}RetrieveVersion()"
#     response2 = requests.get(version_url, headers=headers, auth=auth, verify=False)

#     if response2.status_code == 200:
#         version_info = response2.json()
#         print("Version Dynamics CRM :", version_info.get('Version'))
#     else:
#         print("Erreur lors de la récupération de la version :", response2.status_code)
# else:
#     print("Erreur de connexion à l'API :", response.status_code)


####################################################################################################