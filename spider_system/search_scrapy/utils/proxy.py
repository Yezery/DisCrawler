import requests
proxy_url = "https://proxy.zivye.asia/get/"
delete_url = "https://proxy.zivye.asia/delete/?proxy={}"

def get_proxy():
    """从代理池获取一个代理"""
    try:
        response = requests.get(proxy_url, timeout=5)
        proxy = response.json().get("proxy")
        print(f"Using proxy: {proxy}")
        return proxy
    except Exception as e:
        """从代理池删除失效代理"""
        requests.get(delete_url.format(proxy), timeout=5)
        get_proxy()