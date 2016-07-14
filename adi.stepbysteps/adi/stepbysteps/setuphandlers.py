from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from zope.component import getMultiAdapter

def createSteps(context):
        stepbystep = _createObjectByType('Stepbystep', context, '2', title='NKOTB',
        text='The new bear-band "Nasty Koalas Of Timeless Bliss" has released a debut album with highly sophisticated lyrics, exceptional harmonic roller-coaster-loops and that little something, words cannot describe.\nSo please enjoy, fresh as fish, the single-release: "Step by step (ooh baby)"', #noqa
        description="This is an example description of a step. The description-field is not offered to the user, neither in the form, nor in the views, but we fill it, to see, were it might pop up, and if we want to include it maybe, some day, again.") #noqa
        stepbystep.reindexObject()

        child = _createObjectByType('Stepbystep', stepbystep, '3',
        title='Step One!', text="We can have lots of fun")
        child.reindexObject()
        grandchild = _createObjectByType('Stepbystep', child, '4',
        title='Step Two!', text="There's so much we can do")
        grandchild.reindexObject()
        grandchild = _createObjectByType('Stepbystep', child, '5',
        title='Step Three!', text="It's just you and me")
        grandchild.reindexObject()
        child = _createObjectByType('Stepbystep', stepbystep, '6',
        title='Step Four!', text="I can give you more")
        child.reindexObject()
        child = _createObjectByType('Stepbystep', stepbystep, '7',
        title='Step Five!', text="Don't you know that the time has arrived")
        child.reindexObject()

def createLandingPage(container):
    # Create obj:
    collection = _createObjectByType("Topic", container, 'latest-modified', title='Latest steps', description='An overview of all tickets, sorted by latest modification.')
    
    # Update catalog:
    collection.reindexObject()

    # Set default views:
    container.setDefaultPage('tickets')
    container.setDefaultPage('latest-modified')

    # Set collection-criteria:
    collection_criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    collection_criterion.setValue('Stepbystep')
#            getMultiAdapter((folder, folder.REQUEST, folder.restrictedTraverse('@@plone'), managerAbove, calendar.Assignment()), IPortletRenderer)
 
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
        if (prod['id'] == 'adi.stepbysteps') and (prod['status'] != 'uninstalled'):
            container = _createObjectByType("Folder", context, 'steps', title='Step by step')
            container.reindexObject()
            createSteps(container)
            createLandingPage(container)

def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.stepbysteps.marker.txt') is None:
        return
    createContent(portal)

