import requests


def connection_test(fs_url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; ASUS_Z01QD) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Mobile Safari/537.36'}

    try:
        temp_url = fs_url.split('?')
        url = temp_url[0]
        query = temp_url[1].split('&')
        sign = query[0].split('=')
        t = query[1].split('=')
        querystring = {sign[0]: sign[1], t[0]: t[1]}
    except IndexError:
        return -1, 'Wrong link'

    try:
        with requests.get(url, params=querystring, headers=headers) as response:
            if response.status_code == 200:
                return 1, 'Recording'
            else:
                return 0, 'Offline / pause / lag'

    except Exception as e:
        return -1000, (f'{fs_url}\n'
                       f'\n'
                       f'M3U8 connection test exception : {e}')
