import json

from google.cloud.pubsub_v1 import PublisherClient


class PublisherService:
    def __init__(self):
        self.publisher = PublisherClient()

    def publish_data_to_topic(
        self,
        gcp_project_id: str,
        publish_data: json,
        topic_id: str,
    ) -> list[bool, str]:
        """
        Publishes data to the pubsub topic.

        Parameters:
        gcp_project_id: Google Cloud Platform project id,
        publish_data: data to be sent to the pubsub topic,
        topic_id: unique identifier of the topic the data is published to

        Returns:
        [bool, str]: success status and message
        """
        topic_path = self.publisher.topic_path(gcp_project_id, topic_id)

        if not self._get_topic(topic_path):
            return [False, "Topic not found"]

        self.publisher.publish(
            topic_path, data=json.dumps(publish_data).encode("utf-8")
        )

        return [True, "Data published"]

    def _get_topic(self, topic_path: str) -> bool:
        """
        If the topic does not exist raises 500 global error.
        """
        try:
            self.publisher.get_topic(request={"topic": topic_path})

            return True

        except Exception:
            return False


publisher_service = PublisherService()
