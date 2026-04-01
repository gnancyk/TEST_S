from flask import Blueprint, request, jsonify
from ..services.crm_service import avoir_version_crm

bp = Blueprint('crm', __name__, url_prefix='/crm')

@bp.route('/version', methods=['POST'])
def get_crm_version():
    data = request.get_json() or {}
    crm_url = data.get('crm_url')
    domaine = data.get('domaine', 'univers')
    username = data.get('username', '')
    password = data.get('password', '')

    if not crm_url:
        return jsonify({'status': 400, 'message': 'crm_url requis', 'response': 'N/A'})

    if not username or not password:
        return jsonify({'status': 400, 'message': 'username et password sont requis', 'response': 'N/A'})

    try:
        version = avoir_version_crm(crm_url, domaine, username, password)
        if version == 'N/A' or version.startswith("Erreur"):
            return jsonify({'status': 400, 'message': f"Impossible de récupérer la version CRM : {version}", 'response': 'N/A'})
            
        return jsonify({'status': 200, 'message': f'Version CRM récupérée pour {crm_url}', 'response': version})   
    except Exception as e:
        return jsonify({'status': 500, 'message': f"Erreur interne lors de la récupération de la version : {str(e)}", 'response': 'N/A'})
