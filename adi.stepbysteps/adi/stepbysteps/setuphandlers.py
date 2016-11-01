from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from DateTime import DateTime
from Products.Archetypes.interfaces import IObjectInitializedEvent
from zope.component import getMultiAdapter

def addStep(parent, id_nr):
    id_ = str(id_nr)
    typ = 'Stepbystep'
    title = 'Sample title of ' + id_ 
    text = 'Sample text of ' + id_ + '.'
    #step = _createObjectByType(typ, parent, id_, title=title, text=text)
# We use invokeFactory() instead of _createObjectByType(), because the first
# does, in contradiction to the latter, fire an creation-event, needed for
# our subscriber to take off.
    parent.invokeFactory(typ, id_, title=title, text=text)
    step = parent[id_]
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
    step.setExpirationDate(DateTime())
    step.setTitle('I am an expired step')
    step.reindexObject()

def createStepsLoop(context, n):
    while n > 0:
        addStep(context, n)
        n -= 1

# Assign portlet:
#getMultiAdapter((folder, folder.REQUEST, folder.restrictedTraverse('@@plone'), managerAbove, calendar.Assignment()), IPortletRenderer)

def createContent(context):
    id_ = '0'
    if id_ not in context.keys():
        createSteps(context)

def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.stepbysteps.marker.txt') is None:
        return
    createContent(portal)

