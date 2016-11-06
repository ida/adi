from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot
from adi.devgen.helpers.users import getCurrentUser
from adi.stepbysteps.helpers import getActiveTimes


class View(BrowserView):

    def my_activetimes(self):
        context = aq_inner(self.context)
        current_user = getCurrentUser(self)
        result = getActiveTimes(context, current_user)
        return result
 
    def my_stepbysteps(self):
        """
        Return all stepbysteps where the current
        logged-in user is the responsible person.
        """
        records = []
        criteria = {}
        context = aq_inner(self.context)
        current_user = getCurrentUser(self)
        searchpath = getNavigationRoot(context)

        criteria['path'] = searchpath
        criteria['Type'] = 'Stepbystep'
        criteria['Creator'] = current_user

        brains = self.context.queryCatalog(criteria)

        for brain in brains:
            obj = brain.getObject()
            records.append(obj)

        return records

