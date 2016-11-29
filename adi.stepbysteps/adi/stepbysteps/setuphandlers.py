from DateTime import DateTime
from helpers import getNextId


def addStep(parent):
    id_ = getNextId(parent)
    typ = 'Stepbystep'
    title = 'Sample title of ' + id_ 
    text = 'Sample text of ' + id_ + '.'
    parent.invokeFactory(typ, id_, title=title, text=text)
    step = parent[id_]
    step.reindexObject()
    return step

def addSteps(context, n=3):
    while n > 0:
        if n == 1:
            context = addStep(context)
        else: addStep(context)
        n -= 1
    return context

def createContent(context):
    context = addStep(context)
    context = addSteps(context)
    addSteps(context)
    context = addSteps(context)
    addSteps(context)
    context.setExpirationDate(DateTime())
    context.setTitle('I am an expired step')
    context.reindexObject()

def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.stepbysteps.marker.txt') is None:
        return
    createContent(portal)

