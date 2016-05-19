from z3c.form import interfaces

from zope import schema
from zope.interface import Interface


class ITicketsSettings(Interface):
    """Tickets-config-options for the controlpanel.
    """

    ticket_indexer = schema.Int(title=(u"Ticket index counter"),
                                  description=(u"Unique number for each ticket for referencing-puposes."),
                                  default=-1,)
# Seems that the very first ticket created in a site,
# fires the wired IObjectInitializedEvent twice,
# to compensate index is set to -1 here.
# All following tickets get correctly an Int 
# increased by one, defined in subscribers.py.

