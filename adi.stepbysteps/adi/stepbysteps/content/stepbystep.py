"""Definition of the Archetype-Contenttype 'Stepbystep'.
"""

from Acquisition import aq_inner
from adi.stepbysteps.helpers import getCurrentUser
from adi.stepbysteps.helpers import getEditors

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from plone.app.folder import folder 



# -*- Message Factory Imported Here -*-

from adi.stepbysteps.interfaces import IStepbystep
from adi.stepbysteps.config import PROJECTNAME


from Products.Archetypes.public import DisplayList 


prio = ['low', 'medium', 'high', 'urgent' ]

StepbystepSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField('dependsOn',
        permission="cmf.ManagePortal",
        widget=atapi.StringWidget(
            visible={'edit':'hidden', 'view':'visible'},
        ),
    ),
 
    atapi.StringField('isDependencyOf',
        permission="cmf.ManagePortal",
        widget = atapi.StringWidget(
            visible={'edit':'hidden', 'view':'visible'},
        ),
    ),

    atapi.StringField('responsiblePerson',
		default_method = 'wireGetCurrentUser',
        vocabulary = "wireGetEditors",
        widget = atapi.SelectionWidget(
            visible={'edit':'hidden', 'view':'visible'},
        ),
    ),

    atapi.StringField('priority',
        vocabulary = prio,
	    default = 'medium',
        widget = atapi.SelectionWidget(
            visible={'edit':'hidden', 'view':'visible'},
        ),
    ),

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
# they work well with the python bridge properties.

StepbystepSchema['title'].storage = atapi.AnnotationStorage()
StepbystepSchema['description'].storage = atapi.AnnotationStorage()

StepbystepSchema['description'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}

schemata.finalizeATCTSchema(StepbystepSchema, moveDiscussion=False)


class Stepbystep(folder.ATFolder):
	"""A stepbystep for tasks"""
	implements(IStepbystep)
	meta_type = "Stepbystep"
	schema = StepbystepSchema
	title = atapi.ATFieldProperty('title')
	description = atapi.ATFieldProperty('description')

	def wireGetCurrentUser(self):
		return getCurrentUser(self)

	def wireGetEditors(self):
		return getEditors(self)

atapi.registerType(Stepbystep, PROJECTNAME)
