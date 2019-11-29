from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class Request:
    uuid: str
    session: str
    language: str
    text: str
    parameters: dict

    def __repr__(self):
        return f'{self.text} (lang: {self.language})'


def dict_to_request_object(incoming_dict: dict) -> Request:
    print(incoming_dict)
    query = incoming_dict.get('queryResult', None)
    text = ''
    parameters = {}
    language = 'en'
    if isinstance(query, dict):
        text = query.get('queryText', '')
        parameters = query.get('parameters', {})
        language = query.get('languageCode', 'en')

    session = incoming_dict.get('session', 'failed to load session id')
    uuid = incoming_dict.get('responseId', uuid4())
    return Request(uuid=uuid, session=session, language=language, text=text,
                   parameters=parameters)
