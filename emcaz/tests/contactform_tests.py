"""Tests the contact form feature.
"""


import unittest
from pyramid import testing


class ContactFormTest(unittest.TestCase):
    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)

    def test_has_form(self):
        from emcaz.retail.views import contactform
        context = testing.DummyResource()
        result = contactform(context, self.request)
        self.assertIn('form', result)

    def test_check_email_format(self):
        from emcaz.retail.views import contactform
        context = testing.DummyResource()
        self.request.method = 'POST'
        self.request.params['submit'] = True
        self.request.params['email'] = 'invalid'
        result = contactform(context, self.request)
        self.assertIn('Adresse mail invalide', result['form'])

    def test_valid_form_redirect_to_thankyou(self):
        from emcaz.retail.views import contactform
        from pyramid.httpexceptions import HTTPFound

        context = testing.DummyResource()
        self.request.method = 'POST'
        self.request.params['submit'] = True
        self.request.params['email'] = 'dummy@dummmy.com'
        self.request.params['msg'] = 'msgmsg'
        result = contactform(context, self.request)
        self.assertIsInstance(result, HTTPFound)
        self.assertEqual('/thanks', result.location)

    def tearDown(self):
        testing.tearDown()
