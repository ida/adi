"""Definition of the Archetype-Contenttype 'Ticket'.
"""

from Acquisition import aq_inner
from adi.tickets.helpers import getCurrentUser
from adi.tickets.helpers import getEditors

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from plone.app.folder import folder 



# -*- Message Factory Imported Here -*-

from adi.tickets.interfaces import ITicket
from adi.tickets.config import PROJECTNAME


from Products.Archetypes.public import DisplayList 


prio = ['low', 'medium', 'high', 'urgent' ]

TicketSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField('dependsOn',
        widget=atapi.StringWidget(
            visible={'edit':'hidden', 'view':'visible'},

        ),
    ),
 
    atapi.StringField('isDependencyOf',
        widget = atapi.StringWidget(
            visible={'edit':'hidden', 'view':'visible'},
        ),
    ),

    atapi.StringField('responsiblePerson',
		default_method = 'wireGetCurrentUser',
        vocabulary = "wireGetEditors",
        widget = atapi.SelectionWidget(
        ),
    ),

    atapi.StringField('priority',
        vocabulary = prio,
	    default = 'medium',
        widget = atapi.SelectionWidget(
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

TicketSchema['title'].storage = atapi.AnnotationStorage()
TicketSchema['description'].storage = atapi.AnnotationStorage()

TicketSchema['description'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}

schemata.finalizeATCTSchema(TicketSchema, moveDiscussion=False)


class Ticket(folder.ATFolder):
	"""A ticket for tasks"""
	implements(ITicket)
	meta_type = "Ticket"
	schema = TicketSchema
	title = atapi.ATFieldProperty('title')
	description = atapi.ATFieldProperty('description')

	def wireGetCurrentUser(self):
		return getCurrentUser(self)

	def wireGetEditors(self):
		return getEditors(self)

atapi.registerType(Ticket, PROJECTNAME)
