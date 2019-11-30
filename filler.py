import boto3
import json

database_name = 'dnd_article2'


def add_article(article_name: str, article_text: str, intent_name: str):
    client = boto3.Session(profile_name='kreodont').client('dynamodb')
    stored_dict = client.get_item(
        TableName=database_name,
        Key={
            'name':   {'S': article_name.lower()},
        })
    if 'Item' not in stored_dict:
        stored_dict = {intent_name: {}}
    else:
        stored_dict = json.loads(stored_dict['Item']['value']['S'])

    stored_dict[intent_name]['description'] = article_text

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
    'Испуганное существо совершает с помехой проверки характеристик и броски атаки, пока источник его страха находится в пределах его линии обзора.\n'
    'Существо не способно добровольно приблизиться к источнику своего страха.',
    'condition',
)
