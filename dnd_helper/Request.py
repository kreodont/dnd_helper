from dataclasses import dataclass
from uuid import uuid4
import unicodedata

"""
Incapsulates request from Google Assistant.
Implements couple helper functions
"""

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
        return f'{self.text} (lang: {self.language})\n' \
               f'Parameters: {self.parameters}'


def only_roman_chars(unistr):
    latin_letters = {}

    def is_latin(uchr):
        try:
            return latin_letters[uchr]
        except KeyError:
            return latin_letters.setdefault(
                uchr,
                'LATIN' in unicodedata.name(uchr),
            )

    return all(is_latin(uchr) for uchr in unistr if uchr.isalpha())


def dict_to_request_object(incoming_dict: dict, lambda_mode: bool = True) -> \
        Request:
    query = incoming_dict.get('queryResult', None)
    text = ''
    parameters = {}
    language = 'en'
    intent_name = 'intent_name_not_defined'
    intent_id = 'intent_id_not_defined'
    if isinstance(query, dict):
        text = query.get('queryText', '')
        if only_roman_chars(text):
            language = 'en'
        else:
            language = 'ru'
        parameters = query.get('parameters', {})
        # language = query.get('languageCode', 'en')
        intent = query.get('intent', None)
        if isinstance(intent, dict):
            intent_name = intent.get('displayName', intent_name)
            intent_id = intent.get('name', intent_id)

    session = incoming_dict.get('session', 'failed to load session id')
    uuid = incoming_dict.get('responseId', uuid4())
    return Request(
        uuid=uuid,
        session=session,
        language=language,
        text=text,
        parameters=parameters,
        lamda_mode=lambda_mode,
        intent_name=intent_name,
        intent_id=intent_id,
    )
