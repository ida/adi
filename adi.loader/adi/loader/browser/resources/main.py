from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    index = ViewPageTemplateFile("main.pt")

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def hello(self):
        return "Hello!"

