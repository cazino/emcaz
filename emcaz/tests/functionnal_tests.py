import unittest

from pyramid import testing

# This whole module is probably useless 
# but I needed to write it to get how traversal
# handles default view.
# In the end using "content_type='Root'" 
# on the home_view callable prevents
# the default view from being called with any type of context,
# which is I did not want, and wich is tested here.
#
# WRT to functionnal testing setup, what I do here is horrible
# and I need to find a way to properly setup the whole
# substanced stack instead of cherry picking
# what I setup which ends up in a mess.


class HomeViewTests(unittest.TestCase):

    def _empty_root_factory(self, request):
        return dict()

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('emcaz.include')
        self.config.include('pyramid_chameleon')
        self.config.set_root_factory(self._empty_root_factory)
        app = self.config.make_wsgi_app()
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        """ Clear out the application registry """
        testing.tearDown()

    def test_home_view(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue('cazenave' in res.text)

    def test_home_view_gets_not_called(self):
        from pyramid.httpexceptions import HTTPNotFound
        self.assertRaises(HTTPNotFound, self.testapp.get, '/gibberish')


class HomeViewGetsNotCalledWithAContextTests(unittest.TestCase):

    def _root_factory(self, request):
        return dict(data='data')

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('emcaz.include')
        self.config.include('pyramid_chameleon')
        self.config.set_root_factory(self._root_factory)
        app = self.config.make_wsgi_app()
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        """ Clear out the application registry """
        testing.tearDown()

    def test_home_view_gets_not_called(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue('cazenave' in res.text)
        #from pyramid.httpexceptions import HTTPNotFound
        #self.assertRaises(HTTPNotFound, self.testapp.get, '/data')

    #todo
        