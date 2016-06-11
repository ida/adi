from plone.app.layout.viewlets.content import ContentHistoryView
from Acquisition import aq_inner
from Acquisition import aq_parent
from DateTime import DateTime
from OFS.interfaces import IOrderedContainer
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class View(BrowserView):

    index = ViewPageTemplateFile("main.pt")

    def __call__(self):
        return self.render()

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

    def humanReadableToPrettified(self, human_redable):
        """
        Expects human_redable to be in this format:
        yy:mo:dd:hh:mi:ss
        Returns 00yr 00mo 23dy 14hr 02mi 33sc
        """
        pass

    def computeAge(self):
        """ Return age of item in milliseconds. """
        created = self.context.created().millis()
        created = DateTime().millis() - created
        return created

    def computeActiveTime(self):
        """
        Look for wf-action 'Start' in wf-history
        and accumulate time until next wf-state-transition,
        return sum in milliseconds.
        """
        active_time = 0
        delta = 0
        end_time = 0
        start_time = 0
        context = self.context
        request = context.REQUEST
        history = ContentHistoryView(context, request).workflowHistory()
        for i, story in enumerate(history):
            end_time = 0
            start_time = 0
            if story['state_title'] == 'Active':
                start_time = story['time'].millis()
                if i == 0:
                    end_time = DateTime().millis()
                else:
                    end_time = history[i-1]['time'].millis()
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

