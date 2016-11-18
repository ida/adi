from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from adi.devgen.helpers.content import getChildrenOfType
from adi.devgen.helpers.users import getCurrentUser
from adi.devgen.helpers.times import msToHumanReadable
from adi.devgen.helpers.times import msToPrettified
from adi.devgen.helpers.versioning import getFullHistory
from adi.devgen.helpers.versioning import getWorkflowHistory
from adi.stepbysteps.interfaces import IStepbystepsSettings


def activityEntriesToHtml(entries):
    html = ''
    for entry in entries:
        html += '<ul>' 
        for item in entry:
            html += '<li>'
            if isinstance(item, list):
                for ite in item:
                    html += '<span>' + str(ite) + '</span>'
            else:
                html += item
            html += '</li>'
        html += '</ul>'
    return html

def computeActiveTime(item, user=None):
    """
    Look for wf-action 'Start' in wf-history of item
    and accumulate time until next wf-state-transition,
    return sum in milliseconds.
    """
    MATCH = False
    active_time = 0
    history = getWorkflowHistory(item)
    for i, entry in enumerate(history):
        if (entry['state_title'] == 'Active'):
            MATCH = True
            if user and (entry['actor']['username']) != user:
                MATCH = False
            if MATCH == True:
                start_time = entry['time'].millis()
                if i is 0:
                    end_time = DateTime().millis()
                else:
                    end_time = history[i - 1]['time'].millis()
                delta = end_time - start_time
                active_time += delta
    return active_time

def computeActiveTimes(item, user=None):
    """
    Get accumulated active time of all
    (grand-)childrens in ms, include self.
    """
    path = '/'.join(item.getPhysicalPath())
    item_brains = item.portal_catalog(path={"query": path})
    time = 0
    for item_brain in item_brains:
        item = item_brain.getObject()
        time += computeActiveTime(item, user)
    return time

def getActiveTime(item, user=None):
    time = computeActiveTime(item, user)
    time = msToPrettified(time)
    return time

def getActiveTimes(item, user=None):
    """
    Get accumulated active time of all (grand-)childrens
    in prettified-format, include self.
    """
    time = computeActiveTimes(item, user)
    time = msToPrettified(time)
    return time

def getActivityEntries(items):
    """
    Search workflow-history of each item for entries with the 'Start', 'Pause'
    or 'Stop'-action and compute the time between the start/ and end-actions.
    Return a list of lists in the format like in the first entry below.
    Adds a list-entry for the sum of all activities after each step
    and at lastly also one for the total sum of all steps' activities.
    """
    new_entry = ['Path', 'Title', 'Actor', 'Action', 'Date', 'Time', 'Activity']
    new_entries = [new_entry]
    total_deltas = 0
    for item in items:
        deltas = 0
        end_time = DateTime().millis() # now
        path = '/'.join(item.getPhysicalPath()[2:])
        title = item.Title()
        history = getWorkflowHistory(item)
        for entry in history:
            new_entry = [path, title] # Path + Title
            new_entry.append(entry['actor']['username']) # Actor
            action = entry['transition_title'] # Action
            new_entry.append(action)
            time = entry['time']
            new_entry.append(str(DateTime.Date(time))) # Date
            new_entry.append(str(DateTime.Time(time))) # Time
            time = time.millis()
            delta = last_time - time
            if action == 'Pause' or action == 'Close':
                end_time = time
                new_entry.append('-')
            elif action == 'Start':
                new_entry.append(msToPrettified(delta)) # Delta
                deltas += delta
            else:
                new_entry.append('-')
            new_entries.append(new_entry)
        new_entries.append([path, title, '-', '-', '-',
                            'Total activity:', msToPrettified(deltas)])
        total_deltas += deltas
    new_entries.append(['-', '-', '-', '-', '-',
                        'Total activities:', msToPrettified(total_deltas)])
    return new_entries

def getActivityEntriesRecur(item):
    items = getStepsRecur(item)
    entries = getActivityEntries(items)
    html = activityEntriesToHtml(test_return)
    return html

def getSteps(item):
    """
    Return all item's children of type 'Stepbystep'.
    """
    return getChildrenOfType(item, 'Stepbystep')

def getStepsRecur(item):
    """
    Return all item's children and (grand-)grand-children of type 'Stepbystep'.
    """
    items = []
    brains = item.queryCatalog({
                'path':'/'.join(item.getPhysicalPath()),
                'portal_type':'Stepbystep'
             })
    for brain in brains:
        item = brain.getObject()
        items.append(item)
    return items

def getStepsOfUser(item, user):
    """
    Return all steps of item including self, where the user is
    the responsible person, represented by the Creator-field.
    """
    records = []
    criteria = {}
    criteria['path'] = '/'.join(item.getPhysicalPath())
    criteria['Type'] = 'Stepbystep'
    criteria['Creator'] = user
    brains = self.context.queryCatalog(criteria)
    for brain in brains:
        obj = brain.getObject()
        records.append(obj)
    return records

def handleUrlParams(item):
    """
    Look for search-params in the URL and decide what to do with
    it centrally, here in this definition.
    """
    user = None
    try:
        request = item.REQUEST
        fields = request.form
        for key in fields:
            if key == 'user':
                user = fields[key]
    except:
        print 'no request'
    return getActiveTimes(item, user)

def increaseStepbystepsIndex():
	"""
    Increase and return index-number of
	stepbysteps-registry in controlpanel.
	"""
	registry = getUtility(IRegistry)
	settings = registry.forInterface(IStepbystepsSettings)
	stepbysteps_index = settings.stepbystep_indexer
	new_index = stepbysteps_index + 1
	settings.stepbystep_indexer = new_index
	return new_index

