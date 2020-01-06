from dataclasses import dataclass, field

"""
Incapsulates response to send to Google Assistant.
Implements couple helper functions
"""
@dataclass(frozen=True)
class Response:
    text: str
    header: str = 'No header'
    predictions: list = field(default_factory=list)  # to be drawn at the
    # bottom if any
    # messages: list = field(default_factory=list)
    error: str = None


def response_to_dict(response: Response) -> dict:
    # return {
    #     "fulfillmentText": response.text,
    #     "messages": response.messages,
    # }
    if not response.text:
        return {"fulfillmentText": 'Ничего не найдено'}

    payload = {
        "payload": {
            "google": {
                "expectUserResponse": True,
                "richResponse":       {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": "пожалуйста"
                            }
                        },
                        {
                            "basicCard": {
                                "title":               response.header,
                                # "subtitle": "This is a subtitle",
                                "formattedText":       response.text,
                                # "image": {
                                #   "url": "https://storage.googleapis.com/
                                #   actionsresources/logo_assistant_2x_64dp.png",
                                #   "accessibilityText": "Image alternate text"
                                # },
                                # "buttons":             [
                                #     {
                                #         "title":         "This is a button",
                                #         "openUrlAction": {
                                #             "url": "https://
                                #             assistant.google.com/"
                                #         }
                                #     }
                                # ],
                                # "imageDisplayOptions": "CROPPED"
                            }
                        },
                    ]
                }
            }
        }
    }
    if response.predictions:
        payload['payload']['google']['richResponse']['suggestions'] = []
        for prediction in response.predictions:
            payload['payload']['google']['richResponse'][
                'suggestions'].append({'title': prediction})

    return payload
