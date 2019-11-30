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
    'БЕССОЗНАТЕЛЬНЫЙ',
    '''Находящееся без сознания существо «недееспособно» (см. состояние), не способно перемещаться и говорить, а также не осознаёт своё окружение.
Существо роняет всё, что держит, и падает ничком.
Существо автоматически проваливает спасброски Силы и Ловкости. Броски атаки по существу совершаются с преимуществом.
Любая атака, попавшая по такому существу, считается критическим попаданием, если нападающий находится в пределах 5 фт. от него.
''',
    'condition',
)
