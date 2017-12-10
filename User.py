'''
    Constructor based on SQL value
'''

class User:
    def __init__(self, userInfo):
        self.UID = userInfo['UID']
        self.fname = userInfo['user_fname']
        self.lname = userInfo['user_lname']
        self.username = userInfo['user_username']
        self.email = userInfo['user_email']
        self.password = userInfo['user_password']
    
    def set_fname(self, fname):
        self.fname = fname
    
    def set_lname(self, lname):
        self.lname = lname
    
    def set_username(self, username):
        self.username = username
    
    def set_email(self, email):
        self.email = email
    
    def set_password(self, password):
        self.password = password
    
    def get_uid(self):
        return self.UID
    
    def get_fname(self):
        return self.fname
    
    def get_lname(self):
        return self.lname
    
    def get_username(self):
        return self.username
    
    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password