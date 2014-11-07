from deform import Form, ValidationFailure
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config

from ..resources import Document
from .forms import ContactSchema


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
            'master': get_renderer('templates/master.pt').implementation()}


@view_config(
    name='contact',
    renderer='templates/contact.pt',
)
def contactform(context, request):
    form = Form(ContactSchema().bind(request=request), buttons=('submit',))
    if 'submit' in request.params and request.method == 'POST':
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure as e:
            return dict(form=e.render())

        return HTTPFound('/thanks')
    return dict(form=form.render())
