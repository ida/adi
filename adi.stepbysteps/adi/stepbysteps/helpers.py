from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from adi.devgen.helpers.content import getChildrenOfType
from adi.devgen.helpers.users import getCurrentUser
from adi.devgen.helpers.times import msToHumanReadable
from adi.devgen.helpers.times import msToPrettified
from adi.devgen.helpers.versioning import getWorkflowHistory
from adi.stepbysteps.interfaces import IStepbystepsSettings


def testReturn(item):
    return getActivityEntriesRecur(item)

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
    entry = ['Path', 'Title', 'Actor', 'From', 'To', 'Time']
    entries = [entry]
    step_deltas = steps_deltas = 0
    STEPS_STARTED = False
    now_time = DateTime()
    now_time_str = str(DateTime.Date(now_time)) + ' ' +\
                   str(DateTime.Time(now_time))
    steps_start_str = step_start_str = now_time_str
    for i, item in enumerate(items):
        STEP_STARTED = False
        end_time = DateTime().millis() # now
        end_time_str = 'Is still playing'
        path = '/'.join(item.getPhysicalPath()[2:])
        title = item.Title()
        history = getWorkflowHistory(item)
        for j, story in enumerate(history):
            action = story['transition_title']
            time = story['time']
            time_str = str(DateTime.Date(time)) + ' ' + str(DateTime.Time(time))
            time = time.millis()
            delta = end_time - time
            if action == 'Pause' or action == 'Close':
                end_time = time
                end_time_str = time_str
            elif action == 'Start':
                entry = [path] # Path
                entry.append(title) # Title
                entry.append(story['actor']['username']) # Actor
                entry.append(time_str) # From
                entry.append(end_time_str) # To
                entry.append(msToPrettified(delta)) # Time
                entries.append(entry)
                step_deltas += delta 
                if STEP_STARTED == False:
                    step_start_str = time_str
                    STEP_STARTED = True
                if STEPS_STARTED == False:
                    steps_start_str = step_start_str
                    STEPS_STARTED = True
        if step_deltas > 0 and len(items) > 1:
            if end_time_str == 'Is still playing':
                end_time_str = now_time_str
            entries.append([path, title, 'Total activity:',
                    step_start_str, end_time_str,
                    '<b>' + ' '.join(msToPrettified(step_deltas)) + '</b>'])
        steps_deltas += step_deltas
        step_deltas = 0
    if steps_deltas > 0:
        entries.append(['Report created at:', now_time_str, 'Total activities:',
                    steps_start_str, end_time_str,
                    '<hr><b>' + ' '.join(msToPrettified(steps_deltas)) + '</b>'])
    else: entries = [['No activity has happened, yet.']]
    return entries

def getActivitiesReport(item):
    items = getStepsRecur(item)
    entries = getActivityEntries(items)
    html = activityEntriesToHtml(entries)
    return html

def getActivityReport(item):
    items = [item]
    entries = getActivityEntries(items)
    html = activityEntriesToHtml(entries)
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

def getStepOverdues(item):
    """
    Return all childrens where the expiration-date has passed, include self.
    """
    overdue_steps = []
    steps = getStepsRecur(item)
    for step in steps:
        if step.contentExpired() == True:
            overdue_steps.append(step)
    return overdue_steps

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

