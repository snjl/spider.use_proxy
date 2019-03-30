import requests
from Config import *

headers = {
    # 'Cookie': 'CXID=CC252894B4633CE0DDE67B6B7FEAF161; SUID=707978CA3765860A5C37E18C00027416; SUV=00A54B57B664397C5C639F916EA7D812; ABTEST=0|1553922929|v1; IPLOC=CN3100; weixinIndexVisited=1; JSESSIONID=aaak8cSL-cMVrh07sAjNw; ppinf=5|1553923267|1555132867|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlOEQlOTclRTUlOEMlOTclRTMlODAlODJ8Y3J0OjEwOjE1NTM5MjMyNjd8cmVmbmljazoyNzolRTUlOEQlOTclRTUlOEMlOTclRTMlODAlODJ8dXNlcmlkOjQ0Om85dDJsdUxULXFzNGtzLTFCb3h6WUdKVnQyTVFAd2VpeGluLnNvaHUuY29tfA; pprdig=vAN-GRUzGtZXGMcYJstpX7j79a-mrS63Dy6PvvCWeZiQXJHCd99knRFGvtZELfwfIxycMzc6lyPklpDfkmh7IAzoCvUrEwYJLvhyjBqe_ps_Iyu4A9q_js_XdvtCkgl9BvJnCW7tIyN7u6rOyzYtw3DkrvW-XkZWeVgacOr7Y-I; sgid=19-39884229-AVyeicMPiaTx4viaib9gqZHPn2w; ppmdig=155392326700000006858a9f8b8ec728096be08a837f0ce0; PHPSESSID=i3hiqnrqucg9a74keovae3ml45; SNUID=381BD5006F6AF5388F63B19C709E03AD; sct=5',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

}
proxy = None


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    global proxy
    print("Crawling ", url)
    print("Trying count", count)
    if count >= MAX_COUNT:
        print("tried too many counts")
        return None

    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, proxies=proxies, allow_redirects=False, headers=headers)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 302:
            # 可能跳入异常页或者验证码页，使用代理
            print(302)
            proxy = get_proxy()
            if proxy:
                print("using proxy")
                # count += 1
                return get_html(url, count)
            else:
                print('get proxy failed')
                return None

    except ConnectionError as e:
        print("error occurred ", e.args)
        count += 1
        proxy = get_proxy()
        return get_html(url, count)


if __name__ == '__main__':
    while True:
        url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E5%92%AA%E8%92%99&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=2397&sst0=1553927742286&lkt=1%2C1553927742183%2C1553927742183'
        a = get_html(url, 1)
        # print(a)
