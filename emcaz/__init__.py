from pyramid.config import Configurator

from substanced.db import root_factory



def include(config):
    config.add_static_view('static', 'static', cache_max_age=86400)
    config.scan()

def includeme(config):
    config.include('substanced')
    config.include(include)
    

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.include(includeme)
    return config.make_wsgi_app()
