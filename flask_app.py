from flask import Flask, jsonify, request

from database.db_connector import sql
from modules.messages import message_form
from modules.validation_params import check_params
import requests

app = Flask(__name__)
api_key='bf8f4d7bff7346729ec5bd55856a1591'

correct_params = {
    'users': {
        'POST': ['user_id'],
    },
    'subscriptions': {
        'GET': ['user_id'],
        'POST': ['user_id', 'subscribe'],
        'DELETE': ['user_id', 'subscribe'],
    },
    'news': {
        'GET': ['user_id'],
    },

}

@app.route('/users', methods=['POST'])
def users():
    parametrs = check_params(request, correct_params)
    if parametrs.get('success') == False:
        return jsonify(parametrs)
    user_id = parametrs.get('user_id')
    username = parametrs.get('username')
    user_firstname = parametrs.get('first_name')
    user_lastname = parametrs.get('last_name')
    user_lang = parametrs.get('language')
    user_id = sql('insert', 'insert_user', (
        user_id,
        user_firstname,
        user_lastname,
        username,
        user_lang,
    ))
    if user_id is not None:
        response = message_form(True, '', user_id=user_id)
    else:
        response = message_form(False, 'Добавление пользователя не удалось')
    return jsonify(response)


@ app.route('/subscriptions/<news_type>', methods=['GET', 'POST', 'DELETE'])
def categories(news_type):
    parametrs = check_params(request, correct_params)
    if parametrs.get('success') == False:
        return jsonify(parametrs)

    user_id = parametrs.get('user_id')
    if news_type == 'keywords':
        if request.method == 'GET':
            key_list = sql('select_all', 'get_user_keywords',
                           (user_id,))
            response = message_form(True, '', keywords_list=key_list)

        if request.method == 'POST':
            keyword = parametrs.get('subscribe')
            keyword_id = sql('insert', 'insert_keyword',
                             (user_id, keyword,))
            response = message_form(True, '', keyword_id=keyword_id)

        if request.method == 'DELETE':
            keyword = parametrs.get('subscribe')
            keyword_id = sql('delete', 'delete_keyword',
                             (user_id, keyword,))
            response = message_form(True, '', keyword_id=keyword_id)

    if news_type == 'categories':
        if request.method == 'GET':
            sub_list = sql('select_all', 'get_user_subscribes',
                           (user_id,))
            response = message_form(True, '', subscribes_list=sub_list)

        if request.method == 'POST':
            subscribe = parametrs.get('subscribe')
            subscribe_id = sql('delete', 'add_subscribe',
                             (user_id, subscribe,))
            response = message_form(True, '', subscribe_id=subscribe_id)

        if request.method == 'DELETE':
            subscribe = parametrs.get('subscribe')
            subscribe_id = sql('delete', 'delete_subscribe',
                             (user_id, subscribe,))
            response = message_form(True, '', subscribe_id=subscribe_id)
    return jsonify(response)


@ app.route('/news/<news_type>', methods=['GET'])
def news(news_type):
    parametrs = check_params(request, correct_params)
    if parametrs.get('success') == False:
        return jsonify(parametrs)
    user_id = parametrs.get('user_id')
    if news_type == 'categories':
        subs_list = sql('select_all', 'get_user_subscribes',
                           (user_id,))
        response = []
        for category in subs_list:
            response.append(requests.get('https://newsapi.org/v2/top-headlines?category={0}&apiKey={1}'.format(category[0], api_key)).json().get('articles'))
                
    if news_type == 'keywords':
        subs_list = sql('select_all', 'get_user_keywords',
                           (user_id,))
        search_q_string = []
        for q in subs_list:
            search_q_string.append(q[0])
        search_q_string  = ' OR '.join(search_q_string)
        response = requests.get('https://newsapi.org/v2/top-headlines?q={0}&apiKey={1}'.format(search_q_string, api_key)).json()
    return jsonify(message_form(True, '', articles=response))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
