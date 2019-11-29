from Request import dict_to_request_object
from Response import response_to_dict, Response


def dnd_helper(event: dict, context: dict):
    # print(event)
    print(dict_to_request_object(event), bool(context))
    return response_to_dict(Response('Удачно'))
