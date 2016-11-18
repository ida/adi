from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from adi.stepbysteps import stepbystepsMessageFactory as _
from adi.stepbysteps.helpers import increaseStepbystepsIndex

def handleEditBegun(obj, eve):
    pass#rint obj, eve

def doAfterCancel(obj, eve):
    pass#rint obj, eve

def doAfterSave(obj, eve):
    pass#rint obj, eve

#IObjectInitializedEvent
def setIndexNumber(obj, event):
    """
    Set increased index-number for a stepbystep as id.
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

