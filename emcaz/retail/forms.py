"""Forms and schemas for the retail views.
"""

import colander

from substanced.schema import Schema


class ContactSchema(Schema):

    email = colander.SchemaNode(
        colander.String(),
        validator=colander.Email(msg='Adresse mail invalide'))
    msg = colander.SchemaNode(colander.String())
