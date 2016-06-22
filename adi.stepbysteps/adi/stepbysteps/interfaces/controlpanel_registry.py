from z3c.form import interfaces

from zope import schema
from zope.interface import Interface


class IStepbystepsSettings(Interface):
    """Stepbysteps-config-options for the controlpanel.
    """

    stepbystep_indexer = schema.Int(
      title=(u"Stepbystep index counter"),
      description=(u"Stores the last given stepbystep-id, next stepbystep gets the number plus one as id."),
      default=-1,)
# Seems that the very first stepbystep created in a site,
# fires the wired IObjectInitializedEvent twice,
# to compensate this the index is set to -1 here.
# All following stepbysteps get correctly an Int 
# increased by one, defined in subscribers.py.

