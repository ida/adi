from plone.app.layout.viewlets.content import ContentHistoryView
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    index = ViewPageTemplateFile("main.pt")

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def getChildren(self):
        children_upvotes = 0
        children_downvotes = 0
        children_formatted = ''
        children = self.context.getFolderContents()
        for child in children:
            total = 0
            upvotes = 0
            downvotes = 0
            context = self.context[child.id]
            children_formatted += child['Title']
            history = ContentHistoryView(context, context.REQUEST).workflowHistory()
            for h in history:
                children_formatted += '<br>'
                if h['transition_title'] == 'Upvote':
                    children_formatted += '+1 '
                    upvotes += 1
                elif h['transition_title'] == 'Downvote':
                    children_formatted += '- 1 '
                    downvotes += 1
                else:
                    break # Except intial 'Created'-action.
                children_formatted += h['comments']
                children_formatted += ' ['
                children_formatted += h['actor']['username']
                children_formatted += ']'

            children_formatted += str(upvotes) + ' upvotes and '
            children_formatted += str(downvotes) + ' downvotes, '
            children_formatted += 'give a total of: '
            if upvotes - downvotes > 1:
                children_formatted += str(upvotes - downvotes) + ' upvotes'
            elif upvotes - downvotes < 0:
                children_formatted += str((upvotes - downvotes) * -1) + ' downvotes'
            else:
                children_formatted += str(upvotes - downvotes)
            children_formatted += '.<br>'
            children_upvotes += upvotes
            children_downvotes += downvotes
        children_formatted = "Alltogether it's " + str(children_upvotes) + " upvotes and " + str(children_downvotes) + " downvotes.<br>" + children_formatted
        return children_formatted

    def hello(self):
        hello = self.getChildren()
        return hello

