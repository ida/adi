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
            ticket = _createObjectByType('Ticket', portal, '0', title='Ticktack')
            ticket.reindexObject()
            ticket = _createObjectByType('Ticket', ticket, '1', title='Ticktack', text='Nasowas!')
            ticket.reindexObject()
            ticket = _createObjectByType('Ticket', ticket, '1', title='Ticktack')
            ticket.reindexObject()
            ticket = _createObjectByType('Ticket', ticket, '1', title='Ticktack')
            ticket.reindexObject()
            ticket = _createObjectByType('Ticket', ticket, '1', title='Ticktack')
            ticket.reindexObject()
            ticket = _createObjectByType('Ticket', ticket, '1', title='Ticktack')
            ticket.reindexObject()
            ticket = _createObjectByType('Ticket', ticket, '1', title='Ticktack')
            ticket.reindexObject()

def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.tickets.marker.txt') is None:
        return
    createContent(portal)

