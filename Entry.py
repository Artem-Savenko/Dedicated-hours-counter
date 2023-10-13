class Entry:
    def __init__(self, minutes, activity):
        self.minutes = minutes
        self.activity = activity

    def __repr__(self):
        return self.activity + ' [' + self._getTimeStr() + ']'

    def _getTimeStr(self):
        hours = str(int(self.minutes /60)) + 'h' if int(self.minutes /60) else ''
        mins  = str(self.minutes %60) +'m' if self.minutes %60 else ''
        if hours and mins:
            hours += ' '
        return hours + mins
