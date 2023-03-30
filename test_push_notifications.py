import unittest
from flight_raccoon.push_notifications import PushNotifications
import os
from dotenv import load_dotenv
load_dotenv(".env")

class TestPushNotifications(unittest.TestCase):
    envs = os.environ.copy()

    def test_init(self):
        self.assertEqual(PushNotifications().get_email(), self.envs.get("MY_EMAIL"))