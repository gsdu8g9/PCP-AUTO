import requests
import access_config as conf
import hashlib
import json


def api_request(method, params={}):
    api_server = 'https://api.ok.ru/fb.do?'

    sig_params = ''
    request_params = ''
    for item_key in params.keys():
        sig_params += '{}={}'.format(item_key, params[item_key])
        request_params += '&{}={}'.format(item_key, params[item_key])

    sig_string = 'application_key={}{}method={}{}'.format(conf.PUBLIC_KEY, sig_params, method, conf.SECRET_SESSION_KEY)
    sig = hashlib.md5(sig_string.encode('utf8')).hexdigest()

    request_string = '{}access_token={}&method={}{}&application_key={}&sig={}' \
        .format(api_server, conf.ACCESS_TOKEN, method, request_params, conf.PUBLIC_KEY, sig)
    response = requests.get(request_string).text
    return response


def post(img_path):
    print(api_request('users.getCurrentUser'))


if __name__ == '__main__':
    post(' ')

