"""Tests the contact form feature.
"""


import unittest
from pyramid import testing


class DummyEvent(object):

    def __init__(self, obj, registry):
        self.object = obj
        self.registry = registry


class ContactNotificationTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_mailer.testing')

    def test_email(self):
        # TODO: check methods call on mock objects
        from emcaz.resources import send_contact_notification, Contact
        contact = Contact(email='dummy@dummy.com', msg='dummy msg')
        event = DummyEvent(contact, self.config.registry)
        send_contact_notification(event)
        from pyramid_mailer import get_mailer
        mailer = get_mailer(self.config.registry)
        self.assertEqual(len(mailer.queue), 1)
        self.assertEqual(mailer.queue[0].subject, 'Contact to emcaz')
        self.assertEqual(
            mailer.queue[0].body,
            "%s \n %s" % (contact.email, contact.msg))

    def tearDown(self):
        testing.tearDown()
