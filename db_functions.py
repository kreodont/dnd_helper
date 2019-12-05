import boto3
import json

database_name = 'dnd_article2'


def add_article(*, article_name: str, article_text_ru: str, article_text_en, intent_name: str):
    client = boto3.Session(profile_name='kreodont').client('dynamodb')
    stored_dict = client.get_item(
        TableName=database_name,
        Key={
            'name': {'S': article_name.lower()},
        })
    if 'Item' not in stored_dict:
        stored_dict = {intent_name: {'description': {}}}
    else:
        stored_dict = json.loads(stored_dict['Item']['value']['S'])

    stored_dict[intent_name]['description']['ru'] = article_text_ru
    stored_dict[intent_name]['description']['en'] = article_text_en

    client.put_item(TableName=database_name,
                    Item={
                        'name':  {
                            'S': article_name.lower(),
                        },
                        'value': {
                            'S': json.dumps(stored_dict),
                        }})


def get_article(*, article_name: str) -> dict:
    client = boto3.Session(profile_name='kreodont').client('dynamodb')
    stored_dict = client.get_item(
        TableName=database_name,
        Key={
            'name': {'S': article_name.lower()},
        })
    if 'Item' not in stored_dict:
        stored_dict = {}
    else:
        stored_dict = json.loads(stored_dict['Item']['value']['S'])

    return stored_dict


def update_article_attribute(*, article_name: str, new_text, attribute_name='description', language: str = 'ru', intent=None):
    client = boto3.Session(profile_name='kreodont').client('dynamodb')
    stored_dict = client.get_item(
        TableName=database_name,
        Key={
            'name': {'S': article_name.lower()},
        })
    if 'Item' not in stored_dict:
        stored_dict = {}
    else:
        stored_dict = json.loads(stored_dict['Item']['value']['S'])
    if intent is None:
        if len(stored_dict) != 1:
            raise Exception(f'Intent not specified, but there are more than 1 intent ({stored_dict.keys()}) for article "{article_name}"')
    intent = next(iter(stored_dict))

    new_dict = stored_dict.copy()
    new_dict[intent][attribute_name][language] = new_text
    client.put_item(TableName=database_name,
                    Item={
                        'name':  {
                            'S': article_name.lower(),
                        },
                        'value': {
                            'S': json.dumps(new_dict),
                        }})


# add_article(
#     article_name='СХВАЧЕННЫЙ',
#     article_text_ru=
#     '''Скорость схваченного существа равна 0, и оно не получает выгоды ни от каких бонусов к скорости.
# Состояние оканчивается, если схвативший становится недееспособен (см. состояние).
# Это состояние также оканчивается, если какойлибо эффект выводит схваченное существо из зоны досягаемости того, кто его удерживает, или из зоны удерживающего эффекта. Например, когда существо отбрасывается заклинанием волна грома.
#
# ''',
#     article_text_en=
#     '''A grappled creature’s speed becomes 0, and it can’t benefit from any bonus to its speed.
# The condition ends if the Grappler is incapacitated (see the condition).
# The condition also ends if an effect removes the grappled creature from the reach of the Grappler or Grappling effect, such as when a creature is hurled away by the Thunderwave spell.
#
#     ''',
#     intent_name='condition',
#
# )
print(get_article(article_name='схваченный'))
update_article_attribute(
    article_name='схваченный',
    new_text='Скорость схваченного существа равна 0, и оно не получает выгоды ни от каких бонусов к скорости.  \n'
             'Состояние оканчивается, если схвативший становится недееспособен (см. состояние).  \n'
             'Это состояние также оканчивается, если какойлибо эффект выводит схваченное существо из зоны досягаемости '
             'того, кто его удерживает, или из зоны удерживающего эффекта. Например, когда существо отбрасывается заклинанием волна грома.',
)
print(get_article(article_name='схваченный'))
