from plone.app.registry.browser import controlpanel

from adi.tickets.interfaces import ITicketsSettings

class TicketsSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ITicketsSettings
    label = (u"Tickets settings")
    description = (u"""""")

    def updateFields(self):
        super(TicketsSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(TicketsSettingsEditForm, self).updateWidgets()

class TicketsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = TicketsSettingsEditForm
