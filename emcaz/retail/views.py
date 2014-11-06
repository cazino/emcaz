from pyramid.renderers import get_renderer
from pyramid.view import view_config
from ..resources import Document

#
#   Default "retail" view
#
@view_config(
    renderer='templates/home.pt',
    content_type='Root',
    )
def home_view(context, request):
    return {}

@view_config(
    context=Document,
    renderer='templates/document.pt',
    )
def document_view(context, request):
    return {'title': context.title,
            'body': context.body,
            'master': get_renderer('templates/master.pt').implementation(),
           }

