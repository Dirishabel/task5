from modules.messages import message_form
from flask import Flask, request, jsonify
def check_params(request, correct_params):
    
    if not request.is_json:  
        return message_form(False, 'Неверный формат данных, необходим JSON')
    missing_params = []
    temp_path = request.path.split('/')[1]
    
    for param in correct_params[temp_path][request.method]:
        if param not in request.json.keys():
            missing_params.append(param)
    if missing_params:
        return message_form(False, 'Нехватает параметров: {0}'.format(missing_params))
    return request.json
