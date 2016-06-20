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

            ticket = _createObjectByType('Ticket', portal, '2', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            ticket.reindexObject()

            child = _createObjectByType('Ticket', ticket, '3', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            child.reindexObject()
            childchild = _createObjectByType('Ticket', child, '4', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            childchild.reindexObject()
            childchild = _createObjectByType('Ticket', child, '5', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            childchild.reindexObject()
            childchild = _createObjectByType('Ticket', child, '6', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            childchild.reindexObject()

            child = _createObjectByType('Ticket', ticket, '7', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            child.reindexObject()
            childchild = _createObjectByType('Ticket', child, '8', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            childchild.reindexObject()
            childchild = _createObjectByType('Ticket', child, '9', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            childchild.reindexObject()
            childchild = _createObjectByType('Ticket', child, '10', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            childchild.reindexObject()

            child = _createObjectByType('Ticket', ticket, '11', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            child.reindexObject()
            childchild = _createObjectByType('Ticket', child, '12', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            childchild.reindexObject()
            childchild = _createObjectByType('Ticket', child, '13', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            childchild.reindexObject()
            childchild = _createObjectByType('Ticket', child, '14', title='Ticktack', text="Ein bisschen Text muss sein.", description="Drum tippen wir tagein und tagaus")
            childchild.reindexObject()


def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.tickets.marker.txt') is None:
        return
    createContent(portal)

