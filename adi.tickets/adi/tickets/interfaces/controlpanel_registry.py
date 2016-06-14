from z3c.form import interfaces

from zope import schema
from zope.interface import Interface


class ITicketsSettings(Interface):
    """Tickets-config-options for the controlpanel.
    """

    ticket_indexer = schema.Int(
      title=(u"Ticket index counter"),
      description=(u"Stores the last given ticket-id, next ticket gets the number plus one as id."),
      default=-1,)
# Seems that the very first ticket created in a site,
# fires the wired IObjectInitializedEvent twice,
# to compensate this the index is set to -1 here.
# All following tickets get correctly an Int 
# increased by one, defined in subscribers.py.

