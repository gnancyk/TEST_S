from flask import Blueprint, request, jsonify
from ..services.central_param_service import verifier_lien, verifier_service_soap, avoir_parametres_central_param, avoir_un_parametre

bp = Blueprint('central_param', __name__, url_prefix='/central_param')

@bp.route('/controle', methods=['POST'])
def check_url():
    data = request.get_json() or {}
    url_central_param = data.get('url_central_param')
    
    if not url_central_param:
        return jsonify({'status': 400, 'message': "L'URL central_param est requise", 'response': False})
        
    if (verifier_lien(url_central_param) and verifier_service_soap(url_central_param)):
        return jsonify({'status':200,'message':"Url du centralParam soumis est correct",'response':True})
    elif (verifier_lien(url_central_param) and not verifier_service_soap(url_central_param)):
        return jsonify({'status':400,'message':"Url du centralParam n'est pas un service svc",'response':False})
    else:
        return jsonify({'status':400,'message':"Url du centralParam est incorrect",'response':False})
    
    
@bp.route('/parametres', methods=['POST'])
def get_parameters():
    data = request.get_json() or {}
    url_central_param = data.get('url_central_param')
    
    if not url_central_param:
        return jsonify({'status': 400, 'message': "L'URL central_param est requise", 'response': {}})
        
    try:
        parametres = avoir_parametres_central_param(url_central_param)
        return jsonify({'status':200,'message':"Paramètres recupérés du centralParam",'response':parametres})
    except Exception as e:
        return jsonify({'status': 500, 'message': f"Erreur lors de la récupération des paramètres : {str(e)}", 'response': {}})

@bp.route('/parametre', methods=['POST'])
def get_parameter():
    data = request.get_json() or {}
    url_central_param = data.get('url_central_param')
    param_name = data.get('param_name')
    
    if not url_central_param or not param_name:
        return jsonify({'status': 400, 'message': "url_central_param et param_name sont requis", 'response': {}})
        
    try:
        parametre = avoir_un_parametre(url_central_param, param_name)
        return jsonify({'status': 200, 'message': f"Paramètre {param_name} récupéré", 'response': parametre})
    except Exception as e:
        return jsonify({'status': 500, 'message': f"Erreur lors de la récupération du paramètre : {str(e)}", 'response': {}})   
