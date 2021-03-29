from django.test import TestCase
from django.test.client import Client
from .urls import reverse
import unittest

class MainSiteTestCase(TestCase):
    """
    this tests the main functionalities of the site
    to make sure it works appropiately.
    """

    def test_login_ok(self):
        """
        tests the login is loading ok
        :return: error if any
        """
        endpoint = 'website:login'
        response = self.client.get(reverse(endpoint))
        self.assertTrue(response.status_code == 200,"There's a problem with your request.")

    @unittest.expectedFailure
    def test_dashboard_access_denied(self):
        endpoint = 'website:dashboard'
        response = self.client.get(reverse(endpoint))
        self.assertTrue('dashboard' in response.url, "There's a problem with your request.")
