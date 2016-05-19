from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from zope.component import getMultiAdapter

def createContent(context):
    
    urltool = getToolByName(context, 'portal_url')
    portal = urltool.getPortalObject()
    typestool = getToolByName(context, 'portal_types')
    catalog = getToolByName(context, 'portal_catalog')
    qi = getToolByName(context, 'portal_quickinstaller')
    prods = qi.listInstallableProducts(skipInstalled=False)

    # We only want the following to happen on an initial install,
    # not on a reinstall, which is given if status is uninstalled:
    for prod in prods:
        if (prod['id'] == 'adi.tickets') and (prod['status'] != 'uninstalled'):

            # Create obj:
            folder = _createObjectByType("Folder", portal, 'tickets', title='Tickets')
            collection = _createObjectByType("Topic", folder, 'collection', title='Tickets collection', description='An overview of all tickets, sorted by latest editing, newest first.')
            
            # Update catalog:
            folder.reindexObject()
            collection.reindexObject()

            # Set default views:
#            portal.setDefaultPage('tickets')
            folder.setDefaultPage('collection')

            # Set collection-criteria:
            collection_criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
            collection_criterion.setValue('Ticket')
#            getMultiAdapter((folder, folder.REQUEST, folder.restrictedTraverse('@@plone'), managerAbove, calendar.Assignment()), IPortletRenderer)

def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.tickets.marker.txt') is None:
        return
 #   createContent(portal)
