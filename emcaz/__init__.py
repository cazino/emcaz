from pyramid.config import Configurator

from substanced.catalog import Catalog
from substanced.db import root_factory
from substanced.event import subscribe_created
from substanced.folder import Folder
from substanced.root import Root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.include('substanced')
    config.add_static_view('static', 'static', cache_max_age=86400)
    config.scan()
    return config.make_wsgi_app()


@subscribe_created(Root)
def root_created(event):
    root = event.object
    root['contacts'] = Folder()
