thonimport json

def get_proxy(proxy_config):
    if proxy_config:
        return {"http": proxy_config, "https": proxy_config}
    return None