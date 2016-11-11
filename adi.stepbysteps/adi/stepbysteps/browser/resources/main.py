from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from adi.devgen.helpers.times import getAge
from adi.stepbysteps.helpers import getActiveTime
from adi.stepbysteps.helpers import getActiveTimes
from adi.stepbysteps.helpers import testReturn
from zope.publisher.browser import TestRequest
from zope.site.hooks import getSite as portal


class View(BrowserView):

    index = ViewPageTemplateFile("main.pt")

    def testReturn(self):
        item = aq_inner(self.context)
        return testReturn(item)

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def getActiveTime(self):
        item = self.context
        return getActiveTime(item)

    def getActiveTimes(self):
        item = self.context
        return getActiveTimes(item)

    def getAge(self):
        item = self.context
        return getAge(item)

    def isRootStepbystep(self):
        """
        If a stepbystep lives in the siteroot, it is considered to be a root-stepbystep.
        """
        parent = self.context.aq_parent
        if parent == portal() or parent.Type() != 'Stepbystep':
             return True
        else: return False

    def getStepbystepPosNr(self, step=None):
        """
        Like self.getPosNr(), but only count steps, no other content-types.
        """
        # If no obj is passed, default to context:
        if not step: step = self.context
        if step.Type() == 'Stepbystep':
            step = step.aq_inner
            nr = 0
            parent = step.aq_parent
            #siblings = parent.getFolderContents()
            siblings = parent.listFolderContents(
                        contentFilter={"portal_type" : "Stepbystep"})
            for sibling in siblings:
                nr += 1
                if sibling['id'] == step.id:
                    return nr
        return None

    def getStepbystepPosNrs(self, obj=None):
        """
        Like self.getPosNrs(), but only as long as step is a child of step,
        breaks when other portal_type is detected as parent. Return a nr-path
        like: '2.4.1'.
        """
        nrs = None
        if not obj: obj = self.context
        if obj.Type() == 'Stepbystep':
            nrs = str( self.getStepbystepPosNr(obj) )
            parent = obj.aq_parent
            while parent is not portal():
                nrs = str( self.getStepbystepPosNr(parent) ) + '.' + nrs
                parent = parent.aq_parent
                if parent.Type() != 'Stepbystep':
                    break
            nrs = '.'.join(nrs.split('.')[1:]) # omit nr for root-step
        return nrs

    def getChildSteps(self, context=None):
        if not context: context = self.context
        return context.listFolderContents(
            contentFilter={'portal_type':'Stepbystep'})

    def hasChildren(self, obj=None):
        HAS_CHILDREN = False
        if not obj: obj = self.context
        if len(obj.getFolderContents()) > 0: HAS_CHILDREN = True
        return HAS_CHILDREN

    def hasChildSteps(self, obj=None):
        HAS_CHILDSTEPS = False
        if not obj: obj = self.context
        if len(self.getChildSteps(obj)) > 0: HAS_CHILDSTEPS = True
        return HAS_CHILDSTEPS

