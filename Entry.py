import math


# In this class you should only set last day. First day will be set automatically
# when you set the last day.
# ABBREVIATIONS: dh = Dedicated Hours, cs = Calendar Span
class Entry:
    def __init__(self, minutes, activity):
        self.minutes = minutes
        self.activity = activity
        self.firstDay = None
        self.lastDay = None

    def setLastDay(self, date):
        # set Last day if wasn't set or the date is a later date
        if self.lastDay is None or date > self.lastDay:
            self.lastDay = date

        # set also the 1st day if wasn't set or the date is an earlier date
        if self.firstDay is None or date < self.firstDay:
            self.firstDay = date

    # returns a string that represents this object
    def getAsStr(self, showDedicatedHours, showCalendarSpan):
        dhStr = (self._getDHStr() + ' ') if showDedicatedHours else ''
        csStr = (self._getCSstr() + ' ') if showCalendarSpan else ''
        return dhStr + csStr + self.activity

    # calculates amount of days between first and last day of the activity
    def calcCalendarSpan(self):
        return (self.lastDay - self.firstDay).days + 1


    # ============== ↓↓↓ private methods ↓↓↓ ==============
    def _getDHStr(self):
        return f'[{math.ceil(self.minutes / 60):3}h]'

    def _getCSstr(self):
        return f'{{{str(self.calcCalendarSpan()):>3} days}}'
