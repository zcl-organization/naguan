from functools import wraps
from flask import current_app


def roles_un_permission(url):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            print('set config UNAUTHORIZED_VIEW')
            current_app.config['SECURITY_UNAUTHORIZED_VIEW'] = url
            # print(url)
            return fn(*args, **kwargs)

        return decorator
    return wrapper