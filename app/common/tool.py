import uuid


def get_event_request_id():
    return str(uuid.uuid5(uuid.uuid4(), 'event'))


def get_request_id():
    return str(uuid.uuid5(uuid.uuid4(), 'request'))


def get_task_request_id():
    return str(uuid.uuid5(uuid.uuid4(), 'task'))


def set_return_msg(ok, data, msg, code):
    data = {
        'ok': ok,
        'data': data,
        'msg': msg,
        'code': code

    }
    return data


def set_return_val(ok, data, msg, code, pg=None):
    # type: (object, object, object, object, object) -> object
    if pg:
        data = {
            'ok': ok,
            'data': data,
            'msg': msg,
            'code': code,
            'pg': pg

        }
    else:
        data = {
            'ok': ok,
            'data': data,
            'msg': msg,
            'code': code

        }
    return data
