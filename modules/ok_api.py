import requests
import access_config as conf
import hashlib
import json
import urllib


def api_request(method, params={}):
    api_server = 'https://api.ok.ru/fb.do?'

    sig_keys = []
    for key in params.keys():
        sig_keys.append(key)
    sig_keys.append('method')
    sig_keys = sorted(sig_keys)

    sig_string = 'application_key={}'.format(conf.PUBLIC_KEY)

    for key in sig_keys:
        if key == 'method':
            sig_string += 'method={}'.format(method)
        else:
            sig_string += '{}={}'.format(key, params[key])

    sig_string += conf.SECRET_SESSION_KEY
    sig = hashlib.md5(sig_string.encode('utf8')).hexdigest()
    print(sig_string)

    main_params = {
        'access_token': conf.ACCESS_TOKEN,
        'application_key': conf.PUBLIC_KEY,
        'sig': sig,
        'method': method
    }
    url_string = api_server + urllib.parse.urlencode({**main_params, **params})
    response = requests.get(url_string).text
    return response


def post(img_path='../img/post.png'):
    response_json = api_request('photosV2.getUploadUrl', {'gid': '53233370661082'})
    upload_url = json.loads(response_json)['upload_url']
    photo_id = json.loads(response_json)['photo_ids'][0]
    upload_res = json.loads(requests.post(upload_url, files={'post.png': open(img_path, 'rb')}).text)
    photo_token = upload_res['photos'][photo_id]['token']
    attachment = {
        'media': [
            {
                'type': 'photo',
                'list': [
                    {'id': photo_token}
                ]
            }
        ]
    }
    params = {
        'gid': '53233370661082',
        'type': 'GROUP_THEME',
        'attachment': json.dumps(attachment)
    }
    result = api_request('mediatopic.post', params)
    return isinstance(json.dumps(result), str)


