import requests
import access_config as conf
import hashlib
import json


def api_request(method, params={}):
    api_server = 'https://api.ok.ru/fb.do?'

    sig_keys = []
    for key in params.keys():
        sig_keys.append(key)
    sig_keys.append('method')
    sig_keys = sorted(sig_keys)

    sig_string = 'application_key={}'.format(conf.PUBLIC_KEY)
    request_string = ''

    for key in sig_keys:
        if key == 'method':
            sig_string += 'method={}'.format(method)
            request_string += '&method={}'.format(method)
        else:
            sig_string += '{}={}'.format(key, params[key])
            request_string += '&{}={}'.format(key, params[key])

    sig_string += conf.SECRET_SESSION_KEY
    sig_string = sig_string.replace('+', ' ')
    sig = hashlib.md5(sig_string.encode('utf8')).hexdigest()
    print(sig_string)

    request_string = '{}access_token={}{}&application_key={}&sig={}' \
        .format(api_server, conf.ACCESS_TOKEN, request_string, conf.PUBLIC_KEY, sig)
    response = requests.get(request_string).text
    return response


def post(img_path='../img/post.png'):
    response_json = api_request('photosV2.getUploadUrl', {'gid': '53233370661082'})
    upload_url = json.loads(response_json)['upload_url']
    photos_json = requests.post(upload_url, files={'post.png': open(img_path, 'rb')}).text
    photos_data = json.loads(photos_json)['photos']
    for photo_id in photos_data.keys():
        token = photos_data[photo_id]['token']
        attachment = {
            'media': [
                {
                    'type': 'photo',
                    'list': [
                        {'photo_id': token}
                    ]
                }
            ]
        }
        params = {
            'gid': '53233370661082',
            'type': 'GROUP_THEME',
            'attachment': json.dumps(attachment)
        }
        print(api_request('mediatopic.post', params))


if __name__ == '__main__':
    post()

