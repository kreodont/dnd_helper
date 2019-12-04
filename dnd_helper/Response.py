from dataclasses import dataclass, field


@dataclass(frozen=True)
class Response:
    text: str
    header: str = 'No header'
    messages: list = field(default_factory=list)
    error: str = None


def response_to_dict(response: Response) -> dict:
    # return {
    #     "fulfillmentText": response.text,
    #     "messages": response.messages,
    # }
    formatted_text = response.text if response.text else 'Empty text'
    return {
        "payload": {
            "google": {
                "expectUserResponse": True,
                "richResponse":       {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": "-"
                            }
                        },
                        {
                            "basicCard": {
                                "title":               response.header,
                                # "subtitle": "This is a subtitle",
                                "formattedText":       formatted_text,
                                # "image": {
                                #   "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png",
                                #   "accessibilityText": "Image alternate text"
                                # },
                                # "buttons":             [
                                #     {
                                #         "title":         "This is a button",
                                #         "openUrlAction": {
                                #             "url": "https://assistant.google.com/"
                                #         }
                                #     }
                                # ],
                                # "imageDisplayOptions": "CROPPED"
                            }
                        },
                        # {
                        #     "simpleResponse": {
                        #         "textToSpeech": "-"
                        #     }
                        # }
                    ]
                }
            }
        }
    }
