import colander
import deform.widget

from persistent import Persistent

from substanced.content import content
from substanced.event import subscribe_created
from substanced.property import PropertySheet
from substanced.schema import (
    Schema,
    NameSchemaNode
    )
from substanced.util import renamer

def context_is_a_document(context, request):
    return request.registry.content.istype(context, 'Document')

class DocumentSchema(Schema):
    name = NameSchemaNode(
        editing=context_is_a_document,
        )
    title = colander.SchemaNode(
        colander.String(),
        )
    body = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
        )

class DocumentPropertySheet(PropertySheet):
    schema = DocumentSchema()

@content(
    'Document',
    icon='glyphicon glyphicon-align-left',
    add_view='add_document',
    propertysheets=(
        ('Basic', DocumentPropertySheet),
        ),
    )
class Document(Persistent):

    name = renamer()

    def __init__(self, title='', body=''):
        self.title = title
        self.body = body
        

@content('Contact')
class Contact(Persistent):
    def __init__(self, email='', msg='', dt=''):
        self.email = email
        self.msg = msg
        self.dt = dt

    def get_name(self):
        return "%s-%s" % (self.email, self.dt.strftime("%d%m%Y-%H:%m:%S"))
