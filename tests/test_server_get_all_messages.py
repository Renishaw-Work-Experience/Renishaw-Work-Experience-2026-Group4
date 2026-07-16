import unittest
from unittest.mock import patch

from server import server


class ServerGetAllMessagesTests(unittest.TestCase):
    def test_get_all_messages_accepts_query_params_without_json_body(self):
        client = server.app.test_client()

        with patch("server.server.verifyUser", return_value=True), patch(
            "server.server.database.getAllMessages", return_value=[{"senderID": 7, "content": "hello"}]
        ):
            response = client.get(
                "/listener/get_all_messages",
                query_string={"senderID": "7", "sessionID": "sess-1", "roomID": "1"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["messages"][0]["content"], "hello")


if __name__ == "__main__":
    unittest.main()
