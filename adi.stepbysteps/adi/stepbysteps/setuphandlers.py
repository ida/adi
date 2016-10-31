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
    n = 3
    m = n
    step = addStep(context, 0)
    context = step
    while m > 0:
        createStepsLoop(context, n)
        context = context[str(n)]
        m -= 1

    # Now, let's set an expired expiration-date,
    # to one of the steps, for testing:
    from DateTime import DateTime
    step.setExpirationDate(DateTime())
    step.setTitle('I am an expired step')
    step.reindexObject()

def createStepsLoop(context, n):
    while n > 0:
        addStep(context, n)
        n -= 1

# Assign portlet:
#            getMultiAdapter((folder, folder.REQUEST, folder.restrictedTraverse('@@plone'), managerAbove, calendar.Assignment()), IPortletRenderer)
 
def createOverviews(container):
    # Create collection:
    collection = _createObjectByType("Topic", container, 'latest-modified', title='Latest modified steps', description='An overview of all steps, sorted by latest modification.')
    # Set collection-criteria:
    criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    criterion.setValue('Stepbystep')
    criterion = collection.addCriterion('path', 'ATRelativePathCriterion')
    criterion.setRelativePath('../..')
    # Update catalog:
    collection.reindexObject()
    # Create collection:
    collection = _createObjectByType("Topic", container, 'overdue', title='Overdue steps', description='Steps where the expiration-date has passed by.')
    # Set collection-criteria:
    criterion = collection.addCriterion('expires', 'ATFriendlyDateCriteria')
    criterion.setValue(0)
#    criterion.setDateRange('-')  # This is irrelevant when the date is now, but we set a val anyways?
    criterion.setOperation('less')
    # Enable table-view:
    collection.setCustomView(True)
    # Set fields to show in table-view:
    collection.setCustomViewFields(['Title', 'ExpirationDate'])
    # Set sorting:
    collection.setSortCriterion('expires', 'descending')
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
    id_ = '0'
    if id_ not in context.keys():
        context = _createObjectByType("Stepbystep", context, id_, title='Root step')
        createSteps(context)
        context = _createObjectByType("Folder", context, 'overviews', title='Overviews')
        createOverviews(context)

def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.stepbysteps.marker.txt') is None:
        return
    createContent(portal)

