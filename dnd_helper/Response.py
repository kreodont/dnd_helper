from dataclasses import dataclass, field


@dataclass(frozen=True)
class Response:
    text: str
    messages: list = field(default_factory=list)
    error: str = None


def add_card_to_response(initial_response: Response, formatted_text) -> Response:
    initial_response.messages.append({"formattedText": formatted_text})
    return initial_response

    # messages_dict = {"messages": [
    #     {
    #         "buttons":       [
    #             {
    #                 "openUrlAction": {
    #                     "url": "https://linkUrl.com"
    #                 },
    #                 "title":         "AoG Card Link title"
    #             }
    #         ],
    #         "formattedText": "AoG Card Description",
    # },
    # "platform": "google",
    # "subtitle": "AoG Card Subtitle",
    # "title": "AoG Card Title",
    # "type": "basic_card"
    # }
    # ]
    # }


def response_to_dict(response: Response) -> dict:
    return {"fulfillmentText": response.text, "messages": response.messages}
