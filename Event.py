from Display import Display

class Event:
    def __init__(self, eventInfo):
        self.EID = int(eventInfo['EID'])
        self.uid = int(eventInfo['user_UID'])
        self.name = eventInfo['event_name']
        self.date = eventInfo['event_date']
        self.stime = eventInfo['event_stime']
        self.etime = eventInfo['event_etime']
        self.location = eventInfo['event_location']
        self.description = eventInfo['event_description']
        self.style = Display(self)

    def __lt__(self, other):
        event1 = self.date.replace("-", "") + self.stime.replace(":", "")
        event2 = other.date.replace("-", "") + other.stime.replace(":", "")
        return event1 < event2

    def set_name(self, name):
        self.name = name

    def set_date(self, date):
        self.date = _date

    def set_stime(self, stime):
        self.stime = stime

    def set_etime(self, etime):
        self.etime = etime

    def set_location(self, location):
        self.location = location

    def set_desctiption(self, _description):
        self.description = description
        
    def get_eid(self):
        return self.EID
    
    def get_name(self):
        return self.name

    def get_date(self):
        return self.date

    def get_stime(self):
        return self.stime

    def get_etime(self):
        return self.etime

    def get_location(self):
        return self.location

    def get_description(self):
        return self.description
    
    def get_style(self):
        return self.style