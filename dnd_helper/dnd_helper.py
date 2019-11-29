from Request import dict_to_request_object


def dnd_helper(event: dict, context: dict):
    print(event)
    print(dict_to_request_object(event))
    return {}
