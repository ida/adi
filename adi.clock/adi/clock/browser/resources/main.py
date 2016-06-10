from Products.Five.browser import BrowserView
from DateTime import DateTime

class View(BrowserView):

    def __call__(self):
        return self.render()

    def render(self):
        return self.dates()

    def dateToHumanReadable(self, date):

        FUTUR = False

        now_ms = DateTime().millis()
        date_ms = date.millis()
        diff_ms = now_ms - date_ms

        if diff_ms <= 0:
            FUTUR = True
            diff_ms = diff_ms * -1

        seconds = diff_ms / 1000

        minutes = seconds / 60
        seconds -= minutes * 60
        
        hours = minutes / 60
        minutes -= hours * 60

        days = hours / 24
        hours -= days * 24

        months = days / 30
        days -= months * 30

        years = months / 12
        months -= years * 12

        date = str(years) + 'years '
        date += str(months) + 'months '
        date += str(days) + 'days '
        date += str(hours) + 'hours '
        date += str(minutes) + 'minutes '
        date += str(seconds) + 'seconds '

        return date


    def dates(self):
        dates = '<div id="dates">'
        dates += '<div> Created: '
        date = self.context.created()
        dates += self.dateToHumanReadable(date)
        dates += '</div>'
        dates += '<div>Modified: '
        date = self.context.modified()
        dates += self.dateToHumanReadable(date)
        date = self.context.effective()
        dates += '</div>'
        dates += '<div>Effective: '
        dates += self.dateToHumanReadable(date)
        date = self.context.expires()
        dates += '</div>'
        dates += '<div>Expires: '
        dates += self.dateToHumanReadable(date)
        dates += '</div>'
        dates += '</div>'
        return dates

