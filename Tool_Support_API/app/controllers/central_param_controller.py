from flask import Blueprint, request, jsonify
from ..services.central_param_service import verifier_lien, verifier_service_soap, avoir_parametres_central_param, avoir_un_parametre

bp = Blueprint('central_param', __name__, url_prefix='/central_param')

@bp.route('/controle', methods=['POST'])
def check_url():
    data = request.get_json()
    url_central_param = data.get('url_central_param')
    
    if (verifier_lien(url_central_param) and verifier_service_soap(url_central_param)):
        return jsonify({'status':200,'message':"Url du centralParam soumis est correct",'response':True})
    elif (verifier_lien(url_central_param) and not verifier_service_soap(url_central_param)):
        return jsonify({'status':400,'message':"Url du centralParam n'est pas un service svc",'response':False})
    else:
        return jsonify({'status':400,'message':"Url du centralParam est incorrect",'response':False})
    
    
@bp.route('/parametres', methods=['POST'])
def get_parameters():
    data = request.get_json()
    url_central_param = data.get('url_central_param')
    parametres = avoir_parametres_central_param(url_central_param)
    
    return jsonify({'status':200,'message':"Paramètres recupérés du centralParam",'response':parametres})   

@bp.route('/parametre', methods=['POST'])
def get_parameter():
    data = request.get_json()
    url_central_param = data.get('url_central_param')
    liste_param_name = data.get('liste_param_name')
    print(liste_param_name)
    paramName = data.get('paramName')
    parametres = avoir_un_parametre(url_central_param, paramName)
    
    
    return jsonify({'status':200,'message':"Paramètres recupérés du centralParam",'response':parametres})   

 