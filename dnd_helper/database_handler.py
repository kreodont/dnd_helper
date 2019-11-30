import boto3
import botocore.client
from typing import Optional, Dict
from Request import Request
from Response import Response
import json
# This cache is useful because AWS lambda can keep it's state, so no
# need to restantiate connections again. It is used in get_boto3_client
# function, I know it is a mess, but 100 ms are 100 ms
global_cached_boto3_clients = {}


def get_dynamo_client(
        *,
        lambda_mode: bool,
        profile_name: str = 'kreodont',
        connect_timeout: float = 0.2,
        read_timeout: float = 0.4,
) -> boto3.client:
    client = None

    def closure():
        nonlocal client
        if client:
            return client
        if lambda_mode:
            new_client = boto3.client(
                    'dynamodb',
                    config=botocore.client.Config(
                            connect_timeout=connect_timeout,
                            read_timeout=read_timeout,
                            parameter_validation=False,
                            retries={'max_attempts': 0},
                    ),
            )
        else:
            new_client = boto3.Session(profile_name=profile_name).client(
                'dynamodb')
            return new_client

        # saving to cache to to spend time to create it next time
        client = new_client
        return client

    return closure()


def get_boto3_client(
        *,
        aws_lambda_mode: bool,
        service_name: str,
        profile_name: str = 'kreodont',
        connect_timeout: float = 0.2,
        read_timeout: float = 0.4,
) -> Optional[boto3.client]:
    """
    Dirty function to fetch s3_clients
    :param connect_timeout:
    :param read_timeout:
    :param aws_lambda_mode:
    :param service_name:
    :param profile_name:
    :return:
    """
    known_services = ['translate', 'dynamodb', 's3']
    if service_name in global_cached_boto3_clients:
        print(f'{service_name} client taken from cache!')
        return global_cached_boto3_clients[service_name]

    if service_name not in known_services:
        raise Exception(
                f'Not known service '
                f'name {service_name}. The following '
                f'service names known: {", ".join(known_services)}')

    if aws_lambda_mode:
        client = boto3.client(
                service_name,
                config=botocore.client.Config(
                        connect_timeout=connect_timeout,
                        read_timeout=read_timeout,
                        parameter_validation=False,
                        retries={'max_attempts': 0},
                ),
        )
    else:
        client = boto3.Session(profile_name=profile_name).client(service_name)
        return client, False

    # saving to cache to to spend time to create it next time
    global_cached_boto3_clients[service_name] = client
    return client, False


def fetch_article_text(request: Request, database_name='dnd_article2') -> Response:
    if 'database_client' not in global_cached_boto3_clients:
        global_cached_boto3_clients['database_client'] = get_boto3_client(aws_lambda_mode=request.lamda_mode, service_name='dynamodb')

    parameters_key = f'{request.intent_name}_entity'
    if parameters_key not in request.parameters:
        return Response(text=f'Parameter "{request.intent_name}" not found')

    article_name = request.parameters[parameters_key]

    database_client = global_cached_boto3_clients['database_client']
    result = database_client.get_item(
        TableName=database_name,
        Key={
            'article_name':   {'S': request.parameters['name']},
            # 'date': {'N': 1},
        })

    if 'Item' not in result:
        return Response(text=f'Article "{article_name}" was not found in database')

    items: Dict[dict] = json.loads(result['Item']['value']['S'])
    print(items)
    return Response(text='')
