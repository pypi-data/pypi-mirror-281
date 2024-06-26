from typing import Any
from kbrainsdk.validation.messages import validate_create_subscription, validate_servicebus_message, validate_servicebus_queue, validate_servicebus_topic
from kbrainsdk.apibase import APIBase

class Messages(APIBase):

    def __init__(self, *args: Any, **kwds: Any) -> Any:
        return super().__init__(*args, **kwds)
    
    def publish_message(self, message: str, topic_name: str, application_properties: dict | None = None) -> None:
        payload = {
            "message": message,
            "topic_name": topic_name,
            "application_properties": application_properties
        }
        
        validate_servicebus_message(payload)
        self._publish_message(message, topic_name, application_properties)

    def create_topic(self, topic_name: str) -> None:
        payload = {
            "topic_name": topic_name
        }
        
        validate_servicebus_topic(payload)
        self._create_topic(topic_name)

    def create_queue(self, queue_name: str) -> None:
        payload = {
            "queue_name": queue_name
        }
        validate_servicebus_queue(payload)
        self._create_queue(queue_name)

    def create_subscription(self, topic_name: str, subscription_name: str) -> None:
        payload = {
            "topic_name": topic_name,
            "subscription_name": subscription_name
        }
        validate_create_subscription(payload)
        self._create_subscription(topic_name, subscription_name)

    

