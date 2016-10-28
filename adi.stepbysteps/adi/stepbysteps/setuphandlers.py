from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from zope.component import getMultiAdapter

def addStep(parent, id_nr):
    id_ = str(id_nr)
    typ = 'Stepbystep'
    title = 'Sample title of ' + id_ 
    text = 'Sample text of ' + id_ + '.'
    step = _createObjectByType(typ, parent, id_, title=title, text=text)
    step.reindexObject()
    return step

def createSteps(context):
    step_id_nr = 2

    step = addStep(context, step_id_nr)
    step_id_nr += 1

    addStep(context, step_id_nr)
    step_id_nr += 1

    addStep(context, step_id_nr)
    step_id_nr += 1

    context = step

    step = addStep(context, step_id_nr)
    step_id_nr += 1

    addStep(context, step_id_nr)
    step_id_nr += 1

    addStep(context, step_id_nr)
    step_id_nr += 1

    context = step

    step = addStep(context, step_id_nr)
    step_id_nr += 1

    addStep(context, step_id_nr)
    step_id_nr += 1

    addStep(context, step_id_nr)
    step_id_nr += 1

    # Now, let's set an expired expiration-date,
    # to one of the steps, for testing:
    from DateTime import DateTime
    step.setExpirationDate(DateTime())
    step.setTitle('I am an expired step')
    step.reindexObject()

def createLandingPage(container):
    # Create obj:
    collection = _createObjectByType("Topic", container, 'latest-modified', title='Latest steps', description='An overview of all tickets, sorted by latest modification.')
    
    # Set default views:
    container.setDefaultPage('tickets')
    container.setDefaultPage('latest-modified')

    # Set collection-criteria:
    collection_criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    collection_criterion.setValue('Stepbystep')
    
    date_crit = collection_criterion
    date_crit = collection.addCriterion('expires', 'ATFriendlyDateCriteria')
    date_crit.setValue(0)
    date_crit.setDateRange('-')  # This is irrelevant when the date is now
    date_crit.setOperation('less')

    # Update catalog:
    collection.reindexObject()

# Assign portlet:
#            getMultiAdapter((folder, folder.REQUEST, folder.restrictedTraverse('@@plone'), managerAbove, calendar.Assignment()), IPortletRenderer)
 
def createOverviews(container):
    # Create collection:
    collection = _createObjectByType("Topic", container, 'latest-modified', title='Latest modified steps', description='An overview of all steps, sorted by latest modification.')
    # Set collection-criteria:
    criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    criterion.setValue('Stepbystep')
    # Update catalog:
    collection.reindexObject()
    
    # Create collection:
    collection = _createObjectByType("Topic", container, 'overdue', title='Overdue steps', description='Steps where the expiration-date has passed by.')
    # Set collection-criteria:
    criterion = collection.addCriterion('expires', 'ATFriendlyDateCriteria')
    criterion.setValue(0)
#    criterion.setDateRange('-')  # This is irrelevant when the date is now, but we set a val anyways?
    criterion.setOperation('less')
    # Update catalog:
    collection.reindexObject()


# Example for a new-style-collection:
#    collection = _createObjectByType("Collection", container, 'overdue', title='Overdue steps', description='Steps where the expiration-date has passed by.')
#    query = [{'i': 'portal_type',
#              'o': 'plone.app.querystring.operation.selection.is',
#              'v': ['Stepbystep']},
#             {'i': 'expires',
#              'o': 'plone.app.querystring.operation.date.beforeToday',
#              'v': ''}]
#    collection.setQuery(query)
#    # Update catalog:
#    collection.reindexObject()


def createContent(context):
    
    id_ = 'stepbystep'
    if id_ not in context.keys():
        container = _createObjectByType("Folder", context, 'stepbystep', title='Step by step')
        container.reindexObject()
        createLandingPage(container)
        context = container
        container = _createObjectByType("Stepbystep", context, 'root-step', title='Root step')
        createSteps(container)
        container = _createObjectByType("Folder", context, 'overviews', title='Overviews')
        createOverviews(container)

def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.stepbysteps.marker.txt') is None:
        return
    createContent(portal)

