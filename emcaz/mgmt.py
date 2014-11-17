from webob.exc import HTTPFound
from substanced.sdi import mgmt_view
from substanced.form import FormView

from emcaz.retail.forms import ContactSchema
from emcaz.retail.views import create_contact


@mgmt_view(
    content_type='Root',
    name='add_contact',
    permission='sdi.add-content',
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
)
class AddContactView(FormView):
    title = 'Add Contact'
    schema = ContactSchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        contact = create_contact(self.request, appstruct)
        name = contact.get_name()
        self.context[name] = contact
        loc = self.request.mgmt_path(self.context, name, '@@properties')
        return HTTPFound(location=loc)

