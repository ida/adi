from DateTime import DateTime
from adi.devgen.helpers.content import getChildrenOfType
from adi.devgen.helpers.content import idExists 
from adi.devgen.helpers.times import msToPrettified
from adi.devgen.helpers.versioning import getWorkflowHistory


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
    """
    Get accumulated active-time of item
    in prettified-format.
    """
    time = computeActiveTime(item, user)
    time = msToPrettified(time)
    return time

def getActiveTimes(item, user=None):
    """
    Get accumulated active-time of all (grand-)childrens
    in prettified-format, include self.
    """
    time = computeActiveTimes(item, user)
    time = msToPrettified(time)
    return time

def getActivityEntries(items):
    row = ['Path', 'Title', 'Actor', 'From', 'To', 'Time']
    rows = [row]
    now_date = DateTime()
    now_ms = now_date.millis()
    now_str = str(DateTime.Date(now_date)) + \
        ' ' + str(DateTime.Time(now_date))
    steps_end = now_ms
    steps_end_date = now_date
    steps_deltas = 0
    steps_start = None
    steps_start_str = now_str
    for i, item in enumerate(items):
        end_time = now_ms
        end_time_str = 'Is still playing'
        history = getWorkflowHistory(item)
        item_rows = []
        path = '/'.join(item.getPhysicalPath()[2:])
        step_deltas = 0
        title = item.Title()
        for j, story in enumerate(history):
            action = story['transition_title']
            time = story['time']
            time_str = str(DateTime.Date(time)) + ' ' + str(DateTime.Time(time))
            end_date = time
            time = time.millis()
            delta = end_time - time
            if action == 'Pause' or action == 'Close':
                end_time = time
                end_time_str = time_str
                if steps_end < end_time:
                    steps_end = end_time
                    steps_end_date = end_date
            elif action == 'Start':
                if time < steps_start:
                    steps_start = time
                    steps_start_str = time_str
                item_rows.append([path, title, story['actor']['username'],
			time_str, end_time_str, msToPrettified(delta)])
                step_deltas += delta 

    	# ITEM-TOTAL:
        if len(item_rows) > 0:
            end_time_str = item_rows[0][-2]
            if end_time_str == 'Is still playing':
                end_time_str = now_str
            item_rows.append([
                path,
                title,
                'Total:',
                item_rows[-1][-3],
                end_time_str,
                '<b>' + ' '.join(msToPrettified(step_deltas)) + '</b>'
            ])
            steps_deltas += step_deltas
            rows += item_rows

    # ITEMS-TOTALS:
    item = items[0]
    path = '/'.join(item.getPhysicalPath()[2:])
    title = item.Title()
    rows.append([
            path,
            title,
            'Totals:',
            steps_start_str,
            str(DateTime.Date(steps_end_date)) + ' ' + str(DateTime.Time(steps_end_date)),
            '<b><em>' + ' '.join(msToPrettified(steps_deltas)) + '</em></b>'
        ])
    return rows

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

def getNextId(item):
    nr = 0
    while idExists(item, str(nr)):
        nr += 1
    return str(nr)

def getSteps(item):
    """
    Return all item's children of type 'Step'.
    """
    return getChildrenOfType(item, 'Step')

def getStepsRecur(item):
    """
    Return all item's children and (grand-)grand-children of type 'Step'.
    """
    items = []
    brains = item.queryCatalog({
                'path':'/'.join(item.getPhysicalPath()),
                'portal_type':'Step'
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
    criteria['Type'] = 'Step'
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

