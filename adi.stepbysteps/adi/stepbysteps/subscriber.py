from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from adi.stepbysteps import stepbystepsMessageFactory as _
from adi.stepbysteps.helpers import increaseStepbystepsIndex


def addLastModifiedCollection(step, event):
    # Create collection:
    step.invokeFactory("Topic", 'latest-modified')
    collection = step['latest-modified']
    collection.setTitle('Latest modified steps')
    collection.setDescription('An overview of all steps, sorted by latest modification.')
    # Set collection-criterion 'portal-type' to be 'Stepbystep':
    criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    criterion.setValue('Stepbystep')
    # Set collection-criterion 'relative-path' to be parent,
    # include grand-children and exclude parent in results:
    criterion = collection.addCriterion('path', 'ATRelativePathCriterion')
    criterion.setRelativePath('..')
    criterion.setRecurse(True) # include grand-children
    # Sort results by latest modified item first:
    collection.setSortCriterion('modified', 'descending')
    # Update catalog:
    collection.reindexObject()

def addLastExpiredCollection(step, event):
    # Create collection:
    collection = _createObjectByType("Topic", step, 'overdue',
        title='Overdue steps',
        description='Steps where the expiration-date has passed by.')
    # Sort results by latest expired item first:
    collection.setSortCriterion('expires', 'descending')
    # Enable and thereby also set the table-view as default-template:
    collection.setCustomView(True)
    # Set which columns shall show up in table-view:
    collection.setCustomViewFields(['Title', 'ExpirationDate'])
    # Expiration date passed by:
    criterion = collection.addCriterion('expires', 'ATFriendlyDateCriteria')
    criterion.setValue(0) # now
    criterion.setOperation('less') # older than now
    # Set collection-criterion 'portal-type' to be 'Stepbystep':
    criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    criterion.setValue('Stepbystep')
    # Set collection-criterion 'UID-path' to be parent,
    # include grand-children and exclude parent in results:
    criterion = collection.addCriterion('path', 'ATRelativePathCriterion')
    criterion.setRelativePath('..')
    criterion.setRecurse(True) # include grand-children
    # Update portal-catalog:
    collection.reindexObject()

# Products.Archetypes.interfaces.IObjectInitializedEvent
def addCollections(step, event):
    """
    On creation of a step, add overviews as collections.
    """
    addLastExpiredCollection(step, event)
    addLastModifiedCollection(step, event)

#IObjectInitializedEvent
def setIndexNumber(obj, event):
    """ Set increased index-number for a stepbystep as id.
    """

    context = aq_inner(obj)
    catalog = getToolByName(context, 'portal_catalog')    
    request = context.REQUEST
    index_number = increaseStepbystepsIndex()
    id = str(index_number)
    id_exists = context.portal_catalog.searchResults(REQUEST=request, id=id)

    while id_exists:
        limit = 1000
        while limit > 0:
            index_number = increaseStepbystepsIndex()
            id = str(index_number)
            id_exists = context.portal_catalog.searchResults(REQUEST=request,id = id)
            limit = limit - 1

        else:
            context.plone_utils.addPortalMessage(_(u'Set number as id was aborted after increasing number a 1000 times, instead plone\'s fallback-id was set(id-1, id-2 a.s.o). You might want to resolve this situation, if number-only-strs as stepbystep-ids are crucial to you.'), 'warning')
    else:
        if not id_exists:
            obj.setId(id)
            obj.reindexObject()
    return

