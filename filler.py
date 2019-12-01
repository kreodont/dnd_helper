import boto3
import json

database_name = 'dnd_article2'


def add_article(article_name: str, article_text: str, intent_name: str, lanuage: str):
    client = boto3.Session(profile_name='kreodont').client('dynamodb')
    stored_dict = client.get_item(
        TableName=database_name,
        Key={
            'name':   {'S': article_name.lower()},
        })
    if 'Item' not in stored_dict:
        stored_dict = {intent_name: {'description': {}}}
    else:
        stored_dict = json.loads(stored_dict['Item']['value']['S'])

    stored_dict[intent_name]['description'][lanuage] = article_text

    client.put_item(TableName=database_name,
                    Item={
                        'name': {
                            'S': article_name.lower(),
                        },
                        'value':  {
                            'S': json.dumps(stored_dict),
                        }})


add_article(
    'ИСПУГАННЫЙ',
    '''Испуганное существо совершает с помехой проверки характеристик и броски атаки, пока источник его страха находится в пределах его линии обзора.
Существо не способно добровольно приблизиться к источнику своего страха.
''',
    'condition',
    'ru'
)

add_article(
    'ИСПУГАННЫЙ',
    '''• A frightened creature has disadvantage on ability checks and attack rolls while the source of its fear is within line of sight.
• The creature can’t willingly move closer to the source of its fear.
''',
    'condition',
    'en'
)