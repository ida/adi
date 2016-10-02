from Products.CMFPlone.utils import _createObjectByType

def addItem(context, id_):
    if id_ not in context.keys():
        item = _createObjectByType('Folder', context, id_, title=id_.title())
        return item
    else: return context[id_]

def doOnInstall(context):
    portal = context
    addItem(context, 'emptyFolder')
    context = addItem(context, 'folder')
    context = addItem(context, 'subfolder')
    context = addItem(context, 'subsubfolder')
    context = portal
    addItem(context, 'anEmptyFolder')
    context = addItem(context, 'anotherFolder')
    addItem(context, 'aSubfolder')
    context = addItem(context, 'anotherSubfolder')
    context = addItem(context, 'anotherSubsubfolder')
    context = portal
    addItem(context, 'anotherEmptyFolder')

def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.devcontent.marker.txt') is None:
        return
    doOnInstall(portal)

