from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class Request:
    uuid: str
    session: str
    language: str
    text: str
    parameters: dict
    lamda_mode: bool
    intent_name: str
    intent_id: str

    def __repr__(self):
        return f'{self.text} (lang: {self.language})\nParameters: {self.parameters}'


def dict_to_request_object(incoming_dict: dict, lambda_mode: bool = True) -> \
        Request:
    print(incoming_dict)
    query = incoming_dict.get('queryResult', None)
    text = ''
    parameters = {}
    language = 'en'
    if isinstance(query, dict):
        text = query.get('queryText', '')
        parameters = query.get('parameters', {})
        language = query.get('languageCode', 'en')

    intent_name = 'intent_name_not_defined'
    intent_id = 'intent_id_not_defined'
    intent = incoming_dict.get('intent', None)
    if isinstance(intent, dict):
        intent_name = intent.get('displayName', intent_name)
        intent_id = intent.get('name', intent_id)

    session = incoming_dict.get('session', 'failed to load session id')
    uuid = incoming_dict.get('responseId', uuid4())
    return Request(uuid=uuid, session=session, language=language, text=text,
                   parameters=parameters, lamda_mode=lambda_mode, intent_name=intent_name, intent_id=intent_id)
