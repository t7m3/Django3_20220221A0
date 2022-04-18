from django.test import TestCase

from django.contrib.auth.models import User
from .models import Message

class SnsTests(TestCase):

    def test_check(self):
        usr = User.objects.first()
        self.assertIsNotNone(usr)
        msg = Message.objects.first()
        self.assertIsNotNone(msg)

        