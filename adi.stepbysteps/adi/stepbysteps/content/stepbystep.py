"""Definition of the Archetype-Contenttype 'Stepbystep'.
"""

from adi.stepbysteps.interfaces import IStepbystep
from adi.stepbysteps.config import PROJECTNAME
from plone.app.folder import folder 
from zope.interface import implements
from Acquisition import aq_inner
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.Archetypes.public import DisplayList 


StepbystepSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.TextField('text',
        searchable = True,
        storage = atapi.AnnotationStorage(migrate=True),
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        widget = atapi.RichWidget(
        ),
    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties:
StepbystepSchema['title'].storage = atapi.AnnotationStorage()
StepbystepSchema['description'].storage = atapi.AnnotationStorage()

# Hide description-field of the user in the edit-form or a base-view of a step:
StepbystepSchema['description'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}

schemata.finalizeATCTSchema(StepbystepSchema, moveDiscussion=False)


class Stepbystep(folder.ATFolder):
	"""A stepbystep for tasks"""
	implements(IStepbystep)
	meta_type = "Stepbystep"
	schema = StepbystepSchema
	title = atapi.ATFieldProperty('title')
	description = atapi.ATFieldProperty('description')

atapi.registerType(Stepbystep, PROJECTNAME)
