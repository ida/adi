from Products.CMFCore.utils import getToolByName
from adi.devgen.helpers.users import addUser

def isIniInstall(context):
    qi = getToolByName(context, 'portal_quickinstaller')
    prods = qi.listInstallableProducts(skipInstalled=False)
    for prod in prods:
        if (prod['id'] == 'adi.sampleusers')\
          and (prod['status'] == 'new'):
            return True
    return False

def doOnInstall(context):
    addUser(context, 'dada@example.org')
    addUser(context, 'dede@example.org')
    addUser(context, 'didi@example.org')
    addUser(context, 'dodo@example.org')
    addUser(context, 'dudu@example.org')

def setupVarious(context):
    portal = context.getSite()
    # Looks, if the following file is present, in 'profiles/default',
    # otherwise doOnInstall() would be executed, when running buildout, also:
    if context.readDataFile('adi.sampleusers.marker.txt') is None:
        return

    doOnInstall(portal)
