from Request import dict_to_request_object
from Response import response_to_dict
from database_handler import fetch_article_text


def dnd_helper(event: dict, context: dict) -> dict:
    print(event)
    request = dict_to_request_object(event, bool(context))
    response = fetch_article_text(request)
    return response_to_dict(response)


if __name__ == '__main__':
    print(
        dnd_helper(
            {
                "responseId":    "10e50c03-e05b-465a-b521-49ccd4119ed6-9cc28bb4",
                "queryResult":   {
                    "queryText":                 "об испуганный",
                    "parameters":                {
                        "condition_entity": "Испуганный"
                    },
                    "allRequiredParamsPresent":  True,
                    "fulfillmentText":           "Parameter \"intent_name_not_defined\" not found",
                    "fulfillmentMessages":       [
                        {
                            "text": {
                                "text": [
                                    "Parameter \"intent_name_not_defined\" not found"
                                ]
                            }
                        }
                    ],
                    "intent":                    {
                        "name":        "projects/some-dc42a/agent/intents/7785c88b-8415-40c3-a27a-380994c37d3c",
                        "displayName": "condition"
                    },
                    "intentDetectionConfidence": 0.7332014,
                    "diagnosticInfo":            {
                        "webhook_latency_ms": 1359
                    },
                    "languageCode":              "ru"
                },
                "webhookStatus": {
                    "message": "Webhook execution successful"
                }
            }, {})
    )
