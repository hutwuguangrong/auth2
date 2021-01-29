# python flask auth2 获取 github用户信息

## 1 设置github信息
点头像->Settings->Developer settings->Oauth Apps
->New Oauth App

Application name 随便填

Homepage URL 比如 http://127.0.0.1:5000 按你自己的web项目设置

Application description 随便填

Authorization callback URL 
你在你的web网站上登录，然后会跳到github让你确认授权，这个是你确认授权之后，跳到你的web网站的地址，
比如http:127.0.0.1:5000/oauth/redirect，记下来为redirect_uri

Client ID 记下来

Client secrets 记下来


## 用户授权登录
用户点登录之后，请求@app.route('/login')这个路由，然后就会redirect到
github让你授权登录
```
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
```

## 获取code
redirect的时候，github会把code放在redirect_uri上，从redirect_uri
上获取code就行
```
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
```

## 使用code向github发起post请求，获取accessToken


## 使用accessToken向github发起请求获取到用户信息
