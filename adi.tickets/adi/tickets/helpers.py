from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from adi.tickets.interfaces import ITicketsSettings

def getCurrentUser(self):
	"""Get the current user id or None."""
	context = aq_inner(self)
	mt = getToolByName(context, 'portal_membership')
	if mt.isAnonymousUser():
		return None
	else:
		member = mt.getAuthenticatedMember()
		username = member.getUserName()
		return username

def getEditors(self):
	"""Return everybody, who holds the 
	   local Editor-role.
	"""
	users = [''] # empty string as default
	context = aq_parent(self)
	pu=context.plone_utils

	try: #TODO: exception necessary? siterootcase on ticketcreation, iirc.
		acquired_roles=pu.getInheritedLocalRoles(context)
		local_roles=context.acl_users.getLocalRolesForDisplay(context)
		assigned_roles = acquired_roles + local_roles
	except:
		assigned_roles = []

	for role in assigned_roles:
		if role[2] is not 'group' and 'Editor' in role[1]:
			username = role[0]
			if username not in users:
				users.append(username)

	return users


def increaseTicketsIndex(self):
	""" Increase and return index-number of 
		tickets-registry in controlpanel.
	"""

	registry = getUtility(IRegistry)
	settings = registry.forInterface(ITicketsSettings)
	tickets_index = settings.ticket_indexer
	new_index = tickets_index + 1
	settings.ticket_indexer = new_index

	return new_index
