from flask import Flask, redirect, request
import requests

app = Flask(__name__)

client_id = 'c6c72589846019e46f00'
client_secret = '8ec53567ca353675be6b42e678f551c81ec55f8d'
redirect_uri = 'http://127.0.0.1:5000/oauth/redirect'


@app.route('/login')
def login():
    """将client_id发送给github，github会向redirect_url发送一个
    请求，请求url中包含code参数
    """
    # url1
    url = (f'https://github.com/login/oauth/authorize?'
           f'client_id={client_id}&redirect_uri={redirect_uri}')
    print('url = ', url)
    return redirect(url, 302)


@app.route('/oauth/redirect')
def oauth():
    """获取到code"""
    # url2
    url = 'https://github.com/login/oauth/access_token'
    params = {
        'client_secret': client_secret,
        'client_id': client_id,
        'code': request.args.get('code')
    }
    headers = {'Content-Type': 'application/json'}
    # 发送post请求
    res = requests.post(url, params=params, headers=headers)
    # 获取到access_token
    accessToken = res.text.split('&')[0].split('=')[1]
    # 获取用户信息
    url = 'https://api.github.com/user'
    headers = {
        'accept': 'application/json',
        'Authorization': f'token {accessToken}'
    }
    res = requests.get(url, headers=headers)
    return res.json()


if __name__ == '__main__':
    app.run(debug=True)
