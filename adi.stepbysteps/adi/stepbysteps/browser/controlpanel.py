from plone.app.registry.browser import controlpanel

from adi.stepbysteps.interfaces import IStepbystepsSettings

class StepbystepsSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IStepbystepsSettings
    label = (u"Stepbysteps settings")
    description = (u"""""")

    def updateFields(self):
        super(StepbystepsSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(StepbystepsSettingsEditForm, self).updateWidgets()

class StepbystepsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = StepbystepsSettingsEditForm
