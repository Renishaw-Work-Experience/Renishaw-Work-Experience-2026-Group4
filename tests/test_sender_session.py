import unittest
from unittest.mock import patch

from client import sender


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


class SenderSessionTests(unittest.TestCase):
    def test_request_chat_history_returns_messages_from_json(self):
        session = sender.session(7, "sess-1")
        with patch("client.sender.requests.get", return_value=FakeResponse({"messages": [{"message": "hi"}]})):
            result = session.requestChatHistory(42)

        self.assertEqual(result, [{"message": "hi"}])

    def test_get_rooms_from_user_id_accepts_user_id_argument(self):
        session = sender.session(7, "sess-1")
        with patch("client.sender.requests.get", return_value=FakeResponse({"rooms": [{"roomID": 1, "name": "test"}]})):
            result = session.getRoomsFromUserID(7)

        self.assertEqual(result, [{"roomID": 1, "name": "test"}])


if __name__ == "__main__":
    unittest.main()
