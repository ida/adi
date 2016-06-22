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

    def isRootTicket(self):
        """
        If a ticket lives in the siteroot, it is considered to be a root-ticket.
        """
        if self.context.aq_parent is portal(): return True
        else: return False

    def render(self):
        return self.index()

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
            if len(chunk) == 1:
                chunk = '0' + chunk
            string += chunk
            if i != len(chunks) -1:
                string += ':'

        return string

    def humanReadableToPrettified(self, human_readable):
        """
        Expects human_readable to be in this format:
        yy:mo:dd:hh:mi:ss
        Returns 00yr 00mo 23dy 14hr 02mi 33sc
        """
        pass

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

    def getAge(self):
        age = self.computeAge()
        age = self.msToHumanReadable(age)
        return age

    def getActiveTime(self):
        active_time = self.computeActiveTime()
        active_time = self.msToHumanReadable(active_time)
        return active_time

    def getActiveTimes(self):
        """
        Get accumulated active time of all
        (grand-)childrens, include self.
        """

        active_times = 0

        context = self.context
        path = '/'.join(context.getPhysicalPath())
        item_brains = context.portal_catalog(path={"query": path})

        for item in item_brains:
            active_times += self.computeActiveTime(item)
        active_times = self.msToHumanReadable(active_times) 

        return active_times


    def getPosNr(self, obj=None):
        """Return position of item in parent."""
        # If no obj is passed, default to context:
        if not obj: obj = self.context
        obj = obj.aq_inner
        nr = 0
        parent = obj.aq_parent
        siblings = parent.getFolderContents()
        for sibling in  siblings:
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

    def getTicketPosNr(self):
        """
        Like self.getPosNr(), but except tickets living in the siteroot,
        return None in that case.
        """
        nr = None
        if self.context.aq_parent is not portal():
            nr = self.getPosNr()
        return nr

    def getTicketPosNrs(self):
        """
        Like self.getPosNrs(), but except tickets living in the siteroot,
        meaning e.g. '3.2.7' becomes '2.7'.
        """
        nrs = self.getPosNrs().split('.')
        nrs = '.'.join(nrs[1:])
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

