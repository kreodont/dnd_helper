from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    text: str


def response_to_dict(response: Response) -> dict:
    return {"fulfillmentText": response.text}
