"""Definition of the Subsection content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from Products.ATContentTypes import ATCTMessageFactory as _

from adi.subsection.interfaces import ISubsection
from adi.subsection.config import PROJECTNAME

SubsectionSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField('subsecbody',
        required = False,
        searchable = True,
        primary = True,
        storage = atapi.AnnotationStorage(migrate=True),
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        widget = atapi.RichWidget(
            label = _(u'label_body_text', u'Body Text'),
            description = '',
            allow_file_upload = True)
        ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

SubsectionSchema['title'].storage = atapi.AnnotationStorage()
SubsectionSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    SubsectionSchema,
    folderish=True,
    moveDiscussion=False
)


class Subsection(folder.ATFolder):
    """Folder with textfield for immediate view."""
    implements(ISubsection)

    meta_type = "Subsection"
    schema = SubsectionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Subsection, PROJECTNAME)
