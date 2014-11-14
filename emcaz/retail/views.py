from datetime import datetime

from deform import Form, ValidationFailure
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config
from substanced.root import Root

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
    context=Root,
    name='contact',
    renderer='templates/contact.pt',
)
def contactform(context, request):
    form = Form(ContactSchema().bind(request=request), buttons=('submit',))
    if 'submit' in request.params and request.method == 'POST':
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            contact = create_contact(request, appstruct)
            save_contact(context, contact)
            return HTTPFound("/thanks")
        except ValidationFailure as e:
            return dict(form=e.render())

        return HTTPFound('/thanks')
    return dict(form=form.render())


def create_contact(request, appstruct):
    email = appstruct.get('email')
    msg = appstruct.get('msg')
    return request.registry.content.create(
        'Contact', email, msg, datetime.now())


def save_contact(context, contact):
    contact_name = contact.get_name()
    contacts = context['contacts']
    contacts.add(contact_name, contact)
