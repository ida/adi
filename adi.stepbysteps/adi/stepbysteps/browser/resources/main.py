from Acquisition import aq_parent
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.content import WorkflowHistoryViewlet
from zope.site.hooks import getSite as portal

from zope.publisher.browser import TestRequest
from AccessControl.SecurityManagement import newSecurityManager


class View(BrowserView):

    index = ViewPageTemplateFile("main.pt")

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def isRootStepbystep(self):
        """
        If a stepbystep lives in the siteroot, it is considered to be a root-stepbystep.
        """
        parent = self.context.aq_parent
        if parent == portal() or parent.Type() != 'Stepbystep':
             return True
        else: return False

    def msToHumanReadable(self, ms):
        """
        Convert milliseconds to:
        yy:mo:dd:hh:mi:ss
        """
        string = ''
        ss = ms / 1000
        mi = ss / 60
        ss -= mi * 60
        hh = mi / 60
        mi -= hh * 60
        dd = hh / 24
        hh -= dd * 24
        mo = dd / 30
        dd -= mo * 30
        yy = mo / 12
        mo -= yy * 12
        chunks = [yy, mo, dd, hh, mi, ss]
        for i, chunk in enumerate(chunks):
            chunk = str(chunk)
            string += chunk
            if i != len(chunks) -1:
                string += ':'
        return string

    def humanReadableToPrettified(self, ms):
        """
        """
        pretties = []
        units = ['yrs','mth','dys','hrs','min','sec']

        human_readables = self.msToHumanReadable(ms).split(':')
        for i, human_readable in enumerate(human_readables):
            if human_readable != '0': # omit zero-vals
                if len(human_readable) == 1: # prepend zero if single digit
                    human_readable = '0' + human_readable
                pretties.append(human_readable)
                pretties.append(units[i])
        if len(pretties) > 4: # only take first two non-zero vals
            pretties = pretties[0:4]
        # Prepend zero-val, if there is only one non-zero val, for better
        # readability (same horizontal line-up as the other entries in listview):
        if len(pretties) == 2:
            current_unit = pretties[1]
            previous_unit = units[units.index(current_unit) - 1]
            pretties = ['00', previous_unit] + pretties
        # Dummy val if no time consumed:
        if len(pretties) == 0:
            pretties = ['00', 'min', '00', 'sec']
        return pretties

    def computeAge(self):
        """ Return age of item in milliseconds. """
        created = self.context.created().millis()
        created = DateTime().millis() - created
        return created

    def computeActiveTime(self, brain_obj=None):
        """
        Look for wf-action 'Start' in wf-history
        and accumulate time until next wf-state-transition,
        return sum in milliseconds.
        """
        context = self.context
        if brain_obj: context = brain_obj.getObject()
        active_time = 0
        delta = 0
        end_time = 0
        start_time = 0
        request = context.REQUEST
        history = self.getWorkflowHistory(context)
        for i, entry in enumerate(history):
            if entry['state_title'] == 'Active':
                start_time = entry['time'].millis()
                if i is 0:
                    end_time = DateTime().millis()
                else:
                    end_time = history[i - 1]['time'].millis()
                delta = end_time - start_time
                active_time += delta
        return active_time

    def computeActiveTimes(self):
        """
        Get accumulated active time of all
        (grand-)childrens in ms, include self.
        """
        context = self.context
        path = '/'.join(context.getPhysicalPath())
        item_brains = context.portal_catalog(path={"query": path})
        time = 0
        for item in item_brains:
            time += self.computeActiveTime(item)
        return time

    def getActiveTime(self):
        time = self.computeActiveTime()
        time = self.humanReadableToPrettified(time)
        return time

    def getActiveTimes(self):
        """
        Get accumulated active time of all (grand-)childrens
        in prettified-format, include self.
        """
        time = self.computeActiveTimes()
        time = self.humanReadableToPrettified(time)
        return time

    def getAge(self):
        time = self.computeAge()
        time = self.humanReadableToPrettified(time)
        return time

    def getPosNr(self, obj=None):
        """Return position of item in parent."""
        # If no obj is passed, default to context:
        if not obj: obj = self.context
        obj = obj.aq_inner
        nr = 0
        parent = obj.aq_parent
        siblings = parent.getFolderContents()
        for sibling in siblings:
            nr += 1
            if sibling['id'] == obj.id:
                return nr
        return None

    def getPosNrs(self, obj=None):
        """
        Return position of item in parent as a
        dot-separated path of numbers, like: '2.7.7'
        """
        # If no obj is passed, default to context:
        if not obj: obj = self.context
        nrs = str( self.getPosNr(obj) )
        parent = obj.aq_parent
        while parent is not portal():
            nrs = str( self.getPosNr(parent) ) + '.' + nrs
            parent = parent.aq_parent
        return nrs

    def getStepbystepPosNrs(self, obj=None):
        """
        Like self.getPosNrs(), but only as long as step is a child of step,
        breaks when other portal_type is detected as parent.
        """
        if not obj: obj = self.context
        nrs = str( self.getPosNr(obj) )
        parent = obj.aq_parent
        while parent is not portal():
            nrs = str( self.getPosNr(parent) ) + '.' + nrs
            parent = parent.aq_parent
            if parent.Type() != 'Stepbystep':
                break
        nrs = '.'.join(nrs.split('.')[1:]) # omit nr for root-step
        return nrs

    def getFullHistory(self, obj=None):
        """
        http://docs.plone.org/develop/plone/content/history.html
        """
        history = None
        context = self.context
        if obj: context = obj
        # TODO: user must exist in plonsite ! Zopeadmin can watch anyway.
        #admin = portal().acl_users.getUser('siteadmin')
        #newSecurityManager(request, admin)
        request = TestRequest()
        chv = ContentHistoryViewlet(context, request, None, None)
        # These attributes are needed, the fullHistory() call fails otherwise
        chv.navigation_root_url = chv.site_url = 'http://www.example.org'
        history = chv.fullHistory()
        return history

    def getWorkflowHistory(self, obj=None):
        """
        In contrary to 'context.workflowHistory()', of
        plone.app.viewlets, we can get the wf-history not
        only of the given context, but of any passed obj,
        by passing a fake REQUEST-var and overcome
        permission-restrictions, see:
        http://docs.plone.org/develop/plone/content/history.html
        """
        workflow_history = None
        context = self.context
        if obj: context = obj
        request = TestRequest()
        # TODO: user must exist in plonsite ! Zopeadmin can watch anyway.
        #admin = portal().acl_users.getUser('siteadmin')
        #newSecurityManager(request, admin)
        chv = WorkflowHistoryViewlet(context, request, None, None)
        # These attributes are needed, the fullHistory() call fails otherwise
        chv.navigation_root_url = chv.site_url = 'http://www.example.org'
        workflow_history = chv.workflowHistory()
        return workflow_history

    def hasChildren(self, obj=None):
        HAS_CHILDREN = False
        if not obj: obj = self.context
        if len(obj.getFolderContents()) > 0: HAS_CHILDREN = True
        return HAS_CHILDREN

