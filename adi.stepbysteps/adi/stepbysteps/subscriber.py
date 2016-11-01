from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.statusmessages.interfaces import IStatusMessage
from adi.stepbysteps import stepbystepsMessageFactory as _
from adi.stepbysteps.helpers import increaseStepbystepsIndex

def getNrsOfStr(string):
    """ Returns a list of numbers, any digit following after a hash-character until a non-digit-char occurs, collects the nr, loops until str ends, can be severeal nrs:
        Example: If the str is: 'Bla #27, blubb #12#43, foo #98 7, bar.', then [27,12,43,98] will be returned. Note: The last 7 is not counted, as separated if whitespace (=not a nr).
    """ 
    valids = ['0','1','2','3','4','5','6','7','8','9']
    nrs = []
    nr = ''
    IN_NR = False
    i = 0
    while i < len(string):
        char = string[i]
        if IN_NR and char not in valids or char is '#':
            IN_NR = False
            if nr is not '':
                nrs.append(nr)
                nr = ''
        if char is '#':
            IN_NR = True
        if IN_NR and char is not '#':
            nr += char
        i += 1
    if nr is not '':
        nrs.append(nr)
        nr = ''
    return nrs

#IActionSucceededEvent -> wf-state changed:
def setBlocker(obj, eve):
    """ A stepbystep gets the state 'blocked', extract blockers stepbystepnumber of user's change-comment (collective.wfcomments)
    --->Unblock blocked stepbysteps, if blocker resolves.
    """
    context = aq_inner(obj)
    state = context.portal_workflow.getInfoFor(context, 'review_state')
    #################
    # UNSET BLOCKED #
    #################
    # A stepbystep has been closed:
    if state == 'closed':
        # Check, if tic had blocked other tics:
        is_blocking = obj.getIsDependencyOf()
        if is_blocking is not '':
            # Yes, now for each blocked tic_nr ...
            blocked_nrs = is_blocking.split(',')
            for blocked_nr in blocked_nrs:
                # .. get the refering stepbystep-object:
                criteria = {}
                criteria['id'] = blocked_nr
                blockeds = context.queryCatalog(criteria)
                for b in blockeds: # Get the only result of the list, assuming every id occurs only once.
                    blocked = b.getObject()
                    # We found an item, first remove the blocker's nr of the 'isBlockedBy'-field:
                    is_blocked_by = blocked.getDependsOn()
                    blocker_nrs =  is_blocked_by.split(',')
                    is_blocked_by = ''
                    for blocker_nr in blocker_nrs:
                        if blocker_nr is not obj.getId():
                            is_blocked_by += blocker_nr + ','
                    is_blocked_by = is_blocked_by[:-1] # remove last comma
                    blocked.setDependsOn(is_blocked_by) # set
                    # Now, set the blocker free (change state to 'waiting'):
                    try:
                        context.portal_workflow.doActionFor(blocked, 'pause')
                    except:
                        messages = IStatusMessage(context.REQUEST)
                        messages.add(
                        u"The pause-transisition is not available to the\
                        current state, couldn't switch to state \
                        'waiting'! You might want to adjust the workflow.",
                        type=u'error')
                    # And don't forget to also remove the entry/reference in ourfself, of the 'isBlocking'-field:
                    blocked_nrs =  is_blocking.split(',')
                    is_blocking = ''
                    for blocked_nr in blocked_nrs:
                        if blocked_nr is not blocked.getId():
                            is_blocking += blocked_nr + ','
                    is_blocking = is_blocking[:-1] # remove last comma
                    obj.setIsDependencyOf(is_blocking)


    ###############
    # SET BLOCKED #
    ###############
    if state == 'blocked':
        comment = context.portal_workflow.getInfoFor(context, 'comments')
        if comment is not '': # user-input forced via wfcomments-controlpanel
            nrs = getNrsOfStr(comment) # TODO: force nr in input
            for nr in nrs:

                # Add nr into the stepbystep's 'isBlockedBy'-field:
                is_blocked_by = obj.getDependsOn()
                if is_blocked_by is not '':
                    is_blocked_by += ','
                obj.setDependsOn(is_blocked_by + nr)
                obj.reindexObject()

                # Write the stepbystep's nr into the blocker's 'isBlocking'-field:
                criteria = {}
                criteria['id'] = nr
                blocker = context.queryCatalog(criteria)
                for block in blocker:
                    is_blocking = obj.getIsDependencyOf()
                    if is_blocking is not '':
                        is_blocking += ','
                    block.getObject().setIsDependencyOf(is_blocking + obj.getId())
                    block.getObject().reindexObject()

def addLastModifiedCollection(step):
    # Create collection:
    collection = _createObjectByType("Topic", step, 'latest-modified', title='Latest modified steps', description='An overview of all steps, sorted by latest modification.')

    # SORTING
    # Sort results by latest modified item first:
    collection.setSortCriterion('modified', 'descending')

    # CRITERIA
    # Set collection-criterion 'portal-type':
    criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    criterion.setValue('Stepbystep') # all items of type Stepbystep
    # Set collection-criterion 'relative-path':
    criterion = collection.addCriterion('path', 'ATRelativePathCriterion')
    criterion.setRelativePath('..') # all items in collection-parent
    criterion.setRecurse(True) # include grand-children

    # Update catalog:
    collection.reindexObject()

def addLastExpiredCollection(step):
    # Create collection:
    collection = _createObjectByType("Topic", step, 'overdue', title='Overdue steps', description='Steps where the expiration-date has passed by.')

    # SORTING
    # Sort results by latest expired item first:
    collection.setSortCriterion('expires', 'descending')

    # VIEW
    # Enable and thereby also set the table-view as default-template:
    collection.setCustomView(True)
    # Set which columns shall show up in table-view:
    collection.setCustomViewFields(['Title', 'ExpirationDate'])

    # CRITERIA
    # Set collection-criterion 'expiration-date':
    criterion = collection.addCriterion('expires', 'ATFriendlyDateCriteria')
    criterion.setValue(0) # 0 means now
    criterion.setOperation('less') # all items where exp-date is less than now
    # Set collection-criterion 'portal-type':
    criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    criterion.setValue('Stepbystep') # all items of type Stepbystep
    # Set collection-criterion 'relative-path':
    criterion = collection.addCriterion('path', 'ATRelativePathCriterion')
    criterion.setRelativePath('..') # all items in collection-parent
    criterion.setRecurse(True) # include grand-children

    # Update portal-catalog:
    collection.reindexObject()

# zope.lifecycleevent.IObjectCreatedEvent
def addCollections(step, event):
    """
    On creation of a step, add overviews as collections.
    """
    addLastExpiredCollection(step)
    addLastModifiedCollection(step)

#IObjectInitializedEvent
def setIndexNumber(obj, event):
    """ Set increased index-number for a stepbystep as id.
    """

    context = aq_inner(obj)
    catalog = getToolByName(context, 'portal_catalog')    
    request = context.REQUEST
    index_number = increaseStepbystepsIndex(context)
    id = str(index_number)
    id_exists = context.portal_catalog.searchResults(REQUEST=request, id=id)

    while id_exists:
        limit = 1000
        while limit > 0:
            index_number = increaseStepbystepsIndex(context)
            id = str(index_number)
            id_exists = context.portal_catalog.searchResults(REQUEST=request,id = id)
            limit = limit - 1

        else:
            context.plone_utils.addPortalMessage(_(u'Set number as id was aborted after increasing number a 1000 times, instead plone\'s fallback-id was set(id-1, id-2 a.s.o). You might want to resolve this situation, if number-only-strs as stepbystep-ids are crucial to you.'), 'warning')
    else:
        if not id_exists:
            obj.setId(id)
            obj.reindexObject()
    return


#IObjectModifiedEvent
def setNewOwner(obj, event):
    """ Sets the current responsible person
        to be the only local Owner of a stepbystep.
    """
    context = aq_inner(obj)
    old_owners = context.users_with_local_role('Owner')
    new_owner = context.getResponsiblePerson()

    # Substract Owner-role of everybody:
    for owner in old_owners:
        roles = list(context.get_local_roles_for_userid(owner))
        roles.remove('Owner')

    # Reset other roles:
        if roles:
            context.manage_setLocalRoles(owner, roles)
            context.reindexObjectSecurity()

    # There were no other roles left, simply
    # delete all roles, then:
        else:
            context.manage_delLocalRoles([owner])
            context.reindexObjectSecurity()

    #Set new owner:
    roles = list(obj.get_local_roles_for_userid(new_owner))
    if 'Owner' not in roles: 
        roles.append('Owner')
    obj.manage_setLocalRoles(new_owner, roles)
    obj.reindexObjectSecurity()

    return
