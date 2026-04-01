import requests
from requests_ntlm import HttpNtlmAuth

def avoir_version_crm(crm_url, domaine, username, password):
    """Récupère la version de Dynamics CRM via Web API"""
    web_api_url = f"{crm_url}/api/data/v8.0/"
    
    # Utiliser le domaine passé en argument si l'utilisateur ne le contient pas déjà
    # On s'assure que username est une chaîne pour éviter un crash
    username = str(username) if username else ""
    user_with_domain = f"{domaine}\\{username}" if "\\" not in username else username

    # Authentification NTLM
    auth = HttpNtlmAuth(user_with_domain, password)

    # Appel Web API
    headers = {
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        # Test de connexion à l'API
        response = requests.get(web_api_url, headers=headers, auth=auth, verify=False, timeout=10)
        if response.status_code == 200:
            # Appel de la fonction RetrieveVersion
            version_url = f"{web_api_url}RetrieveVersion()"
            response2 = requests.get(version_url, headers=headers, auth=auth, verify=False, timeout=10)

            if response2.status_code == 200:
                version_info = response2.json()
                return version_info.get('Version', 'N/A')
            else:
                return f"Erreur RetrieveVersion: {response2.status_code}"
        else:
            return f"Erreur Endpoint: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion : {str(e)}"
