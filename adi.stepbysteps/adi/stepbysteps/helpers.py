from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from adi.devgen.helpers.content import getChildrenOfType
from adi.devgen.helpers.users import getCurrentUser
from adi.devgen.helpers.times import msToHumanReadable
from adi.devgen.helpers.times import humanReadableToPrettified
from adi.devgen.helpers.versioning import getWorkflowHistory
from adi.stepbysteps.interfaces import IStepbystepsSettings


def formatActivityEntries(entries):
    """
    Expects a tuple of entries of the workflow-history.
    Return a list of lists showing user, start/end-action, date, time and the
    time consumed betweeen each entry-pair from to start and as last entry a
    sum of all of these.
    """
    formatted_entry = ['User', 'Action', 'Date', 'Time', 'Delta']
    formatted_entries = [formatted_entry]
    deltas = delta = end_time = start_time = 0
    for i, entry in enumerate(entries):
        # Collect user:
        formatted_entry = [entry['actor']['username']]
        # Collect action:
        action = entry['transition_title']
        formatted_entry.append(action)
        # Collect time:
        time = entry['time']
        formatted_entry.append(str(DateTime.Date(time)))
        formatted_entry.append(str(DateTime.Time(time)))
        time = time.millis()

        # Compute and collect delta:
        if action == 'Pause' or action == 'Stop':
            end_time = time
        elif action == 'Start':
            start_time = time
        if end_time != 0 and start_time != 0:
            if end_time == start_time:
                end_time = DateTime().millis()
            delta = end_time - start_time
        if delta != 0:
            deltas += delta
            delta = humanReadableToPrettified(delta)
            formatted_entry.append(delta)
            delta = end_time = start_time = 0
        else:
            formatted_entry.append('')

        # Collect whole new entry:
        formatted_entries.append(formatted_entry)

    # Collect total delta:
    formatted_entries.append(
        ['0', '0', '0', '0', humanReadableToPrettified(deltas)])
    formatted_entries.append(
        ['0', '0', '0', '0', msToHumanReadable(deltas)])

    return formatted_entries

def activityEntriesToHtml(entries):
    html = ''
    for i, entry in enumerate(entries):
        html += '<ul><li>' + str(i) + '</li>'
        for item in entry:
            html += '<li>'
            if type(item) == list:
                for ite in item:
                    html += '<span>' + ite + ' </span>'
            else:
                html += str(item)
            html += '</li>'
        html += '</ul>'
    return html

def getActivityEntries(item):
    entries = getWorkflowHistory(item)
    entries = formatActivityEntries(entries)
    entries = activityEntriesToHtml(entries)
    return entries

def testReturn(item):
    test_return = getActivityEntries(item)
    items = []
    items_brain = item.getFolderContents()
    for item_brain in items_brain:
        item = item_brain.getObject()
        test_return += getActivityEntries(item)
        items.append(item_brain)
    return test_return

#######################################################
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
    time = humanReadableToPrettified(time)
    return time

def getActiveTimes(item, user=None):
    """
    Get accumulated active time of all (grand-)childrens
    in prettified-format, include self.
    """
    time = computeActiveTimes(item, user)
    time = humanReadableToPrettified(time)
    return time

def getSteps(item):
    """Return all item's children of type 'Stepbystep'."""
    return getChildrenOfType(item, 'Stepbystep')

def getStepsOfUser(item, user):
    """
    Return all children including self, where the user is
    the responsible person, represented by the Creator-field.
    """
    records = []
    criteria = {}
    criteria['path'] = '/Plone'
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

