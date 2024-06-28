from osbot_utils.utils.Http import http_request

# add to Http.py
def is_url_online(target):
    try:
        http_request(target, method='HEAD')
        return True
    except:
        return False