import requests
from urllib.parse import urlparse
from zeep import Client

def verifier_lien(url):
    parsed_url = urlparse(url)

    if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc:
        # print("URL valide")
        return True
    else:
        # print("URL invalide")
        return False
        

def verifier_service_soap(url):
    try:
        # Envoi d'une requête GET pour tester l'accès au service
        response = requests.get(url)
        
        # Vérifie si la réponse est OK (status code 200)
        if response.status_code == 200:
            # Vérifie si la réponse contient quelque chose d'attendu pour un service SVC
            if "Service" in response.text or "WCF" in response.text:
                # print("C'est un service SVC.")
                return True
            else:
                # print("Réponse non spécifique au service SVC.")
                return False
        else:
            # print(f"Échec de la connexion au service SVC, code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        # print(f"Erreur lors de la requête: {e}")
        return False


def avoir_configuration_central_param(url):
    ext_param = '?wsdl'
    wsdl = url + ext_param  # ou ton vrai chemin
    client = Client(wsdl=wsdl)

    # print("=== Services disponibles ===")
    for service in client.wsdl.services.values():
        service_name = service.name
        # print(f"Service: {service.name}")
        for port in service.ports.values():
            # print(f"  Port: {port.name}")
            service_port = port.name
            operations = port.binding._operations
            # print("  Opérations disponibles:")
            # for operation in operations:
                # print(f"    - {operation}")
    
    return service_name, service_port

def avoir_parametres_central_param(url, parametres = []):
    service_name , service_port =avoir_configuration_central_param(url)
    ext_param = '?wsdl'
    service_url = url + ext_param
     
    client = Client(wsdl=service_url)
    service = client.bind(service_name,service_port)
    # service = client.bind('CentralisationParam', 'BasicHttpBinding_ICentralisationParam')

    # 3. Récupération des types
    ArrayOfParameter = client.get_type('ns2:ArrayOfParameter')
    Parameter = client.get_type('ns2:Parameter')

    # 4. Construction de la liste des paramètres
    # params_list = [
    #     # Parameter(ParamName='CrmConnectionString'),  # Adapte les noms si besoin
    #     # Parameter(Name='Type', Value='X')
    # ]
    params_list = parametres

    # 5. Création de l'objet attendu par le service
    array_of_params = ArrayOfParameter(params_list)

    # 6. Appel de la méthode SOAP avec le bon paramètre
    response = service.GetParameter(_prameters=array_of_params)
    
    # return convert_array_of_parameter_to_list(response)

    parametres = {}
    for t in response['ListOfParmeters']['Parameter']:
        parametres[t['ParamName']] = t['ParamValue']
    return parametres

def avoir_un_parametre(url, paramName):
    service_name , service_port =avoir_configuration_central_param(url)
    ext_param = '?wsdl'
    service_url = url + ext_param
     
    client = Client(wsdl=service_url)
    service = client.bind(service_name,service_port)
    # service = client.bind('CentralisationParam', 'BasicHttpBinding_ICentralisationParam')

    # 3. Récupération des types
    ArrayOfParameter = client.get_type('ns2:ArrayOfParameter')
    Parameter = client.get_type('ns2:Parameter')

    # 4. Construction de la liste des paramètres
    params_list = [
        Parameter(ParamName=f'{paramName}'),  # Adapte les noms si besoin
        # Parameter(Name='Type', Value='X')
    ]

    # 5. Création de l'objet attendu par le service
    array_of_params = ArrayOfParameter(params_list)

    # 6. Appel de la méthode SOAP avec le bon paramètre
    response = service.GetParameter(_prameters=array_of_params)
    
    # return convert_array_of_parameter_to_list(response)

    parametres = {}
    
    if ';' in response['ListOfParmeters']['Parameter'][0]['ParamValue']:
        for elt in response['ListOfParmeters']['Parameter'][0]['ParamValue'].split(';'):
            parametres[elt.split('=')[0]] = elt.split('=')[1]
    else:
        parametres[response['ListOfParmeters']['Parameter'][0]['ParamName']] = response['ListOfParmeters']['Parameter'][0]['ParamValue']
    
    return parametres


# def avoir_les_parametre(url, liste_paramName):
#     service_name , service_port =avoir_configuration_central_param(url)
#     ext_param = '?wsdl'
#     service_url = url + ext_param
     
#     client = Client(wsdl=service_url)
#     service = client.bind(service_name,service_port)
#     # service = client.bind('CentralisationParam', 'BasicHttpBinding_ICentralisationParam')

#     # 3. Récupération des types
#     ArrayOfParameter = client.get_type('ns2:ArrayOfParameter')
#     Parameter = client.get_type('ns2:Parameter')

#     params_list =  []
#     # 4. Construction de la liste des paramètres
#     for paramName in liste_paramName:
#         params_list.append(Parameter(ParamName=f'{paramName}'))
#             # Parameter(Name='Type', Value='X')
  
#     print(params_list)
#     # 5. Création de l'objet attendu par le service
#     array_of_params = ArrayOfParameter(params_list)

#     # 6. Appel de la méthode SOAP avec le bon paramètre
#     response = service.GetParameter(_prameters=array_of_params)
    
#     # return convert_array_of_parameter_to_list(response)

#     parametres = {}
    
#     if ';' in response['ListOfParmeters']['Parameter'][0]['ParamValue']:
#         for elt in response['ListOfParmeters']['Parameter'][0]['ParamValue'].split(';'):
#             parametres[elt.split('=')[0]] = elt.split('=')[1]
#     else:
#         parametres[response['ListOfParmeters']['Parameter'][0]['ParamName']] = response['ListOfParmeters']['Parameter'][0]['ParamValue']
    
#     return parametres
