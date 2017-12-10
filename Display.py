from datetime import time, timedelta

class Display:
    def __init__(self, event):
        self.stime = event.stime
        self.etime = event.etime
        self.top = self.get_top()
        self.height = self.get_height()

    def __repr__(self):
        style = "top: " + str(self.top) + "px; "
        style += "height: " + str(self.height) + "px; "
        return style

    def get_top(self):
        stime = timedelta(hours=int(self.stime[0:2]), minutes=int(self.stime[3:5]))
        return int(3.2 * (stime.total_seconds() // 60))

    def get_height(self):
        stime = timedelta(hours=int(self.stime[0:2]), minutes=int(self.stime[3:5]))
        etime = timedelta(hours=int(self.etime[0:2]), minutes=int(self.etime[3:5]))
        ttime = etime - stime
        return int(3.2 * (ttime.total_seconds() // 60))