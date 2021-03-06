from django.test import TestCase
from django.core.urlresolvers import reverse


class SessionViewTests(TestCase):
    def test_open_session_list(self):
        response = self.client.get(reverse('session:servers'))
        self.assertEqual(response.status_code, 200)
