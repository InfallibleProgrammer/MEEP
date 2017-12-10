from User import User
from Event import Event
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, create_engine, MetaData, Table, select, or_, and_, join
from sqlalchemy.engine import reflection
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date as today
from time import strftime, strptime, localtime

# DELETE
logged_in = False

#sql server connection
engine =  create_engine("SQL DATABASES LINK GOES HERE")
inspector = inspect(engine)
meta = MetaData(engine,reflect=True)
tbl_user = meta.tables['tbl_user']
tbl_events = meta.tables['tbl_events']
tbl_friends = meta.tables['tbl_friends']

def connectDB(query):
    conn = engine.connect()
    res = conn.execute(query)
    engine.dispose()
    return list(res)

def commitDB(table1, data):
    conn = engine.connect()
    conn.execute(table1.insert(), data)


def getUser(key):
    if type(key) == int or type(key) = long:
        query = select([tbl_user]).where(tbl_user.c.UID == key)
        userInfo = connectDB(query)
    else:
        query = select([tbl_user]).where(tbl_user.c.user_username == key)
        userInfo = connectDB(query)
    return User(userInfo[0])

def getEvent(EID, date=None):
    if date:
        query = select([tbl_events]).where(and_(
                                                tbl_events.c.EID == EID,
                                                tbl_events.c.event_date == date
                                                ))
    else:
        query = select([tbl_events]).where(tbl_events.c.EID == EID)
    eventInfo = connectDB(query)
    return Event(eventInfo[0])

def getEvents(UID, date=None):
    eventsList = []
    if date:
        query = select([tbl_events]).where(and_(
                                                tbl_events.c.user_UID == UID,
                                                tbl_events.c.event_date == date
                                                )).order_by(tbl_events.c.event_date)
    else:
        current_date = str(today.today())
        query = select([tbl_events]).where(and_(
                                            tbl_events.c.user_UID == UID,
                                            tbl_events.c.event_date >= current_date
                                            )).order_by(tbl_events.c.event_date)
    eventsInfo = connectDB(query)
    for eventInfo in eventsInfo:
        eventsList.append(Event(eventInfo))
    eventsList.sort()
    return eventsList

def getFriends(UID):
    friendsList = []
    query = select([tbl_friends]).where(tbl_friends.c.friend_uid1 == UID)
    friendsInfo = connectDB(query)
    for friend in friendsInfo:
        friendsList.append(getUser(friend['friend_uid2']))
    return friendsList
        
def checkLogin(user_username, user_password):
    query = select([tbl_user.c.user_password]).where(tbl_user.c.user_username == user_username)
    hashed_password = connectDB(query)
    if hashed_password and check_password_hash(hashed_password[0][0], user_password):
        authenticated = True
    else:
        authenticated = False
    return authenticated

def createUser(userInfo):   
    userInfo = dict(userInfo)
    user_username = userInfo['user_username']
    user_email = userInfo['user_email']

    userInfo['user_password'] = generate_password_hash(userInfo['user_password'][0])

    query = select([tbl_user]).where(
                                    or_(
                                        tbl_user.c.user_username == user_username, 
                                        tbl_user.c.user_email == user_email
                                        ))
    if connectDB(query):
        success = False
    else:
        commitDB(tbl_user, userInfo)
        success = True
    return success

def createEvent(UID, eventInfo):
    eventInfo = dict(eventInfo)
    eventInfo['user_UID'] = UID
    commitDB(tbl_events, eventInfo)    
    success = True
    return success

def editEvent(eventInfo, EID):   
    conn = engine.connect()
    res = tbl_events.update().values(eventInfo).where(tbl_events.c.EID == EID)
    conn.execute(res)
    engine.dispose()
    return True

def deleteEvent(EID):
    d = tbl_events.delete(tbl_events.c.EID == EID)
    d.execute()

def checkFriend(friend1, friend2):
    query = select([tbl_friends]).where(
                                        and_ (
                                            tbl_friends.c.friend_uid1 == friend1, 
                                            tbl_friends.c.friend_uid2 == friend2
                                        ))
    if friend1 == friend2:
        return True
    elif connectDB(query):
        return True
    else:
        return False

def addFriend(friend1, friend2):
    conn = engine.connect()
    conn.execute(tbl_friends.insert(), friend_uid1 = friend1, friend_uid2 = friend2)
    engine.dispose()


def removeFriend(friend1, friend2):
    query = select([tbl_friends]).where(and_ (tbl_friends.c.friend_uid1 == friend1, tbl_friends.c.friend_uid2 == friend2))
    if connectDB(query):
        d = tbl_friends.delete(and_(tbl_friends.c.friend_uid1 == friend1, tbl_friends.c.friend_uid2 == friend2))
        d.execute()

def compareSchedules(all_events):
    conflict = []

    for event in all_events:
        stime = int(event.get_stime().replace(':', ''))
        etime = int(event.get_etime().replace(':', ''))

        conflict.append(range(stime, etime))
    
    times = []
    for hour in range(24):
        for minute in range(0, 60, 15):
            id_num = "_{:02}{:02}".format(hour, minute);
            time = strftime("%I:%M %p", strptime(
                            "{:02}:{:02}".format(hour, minute), "%H:%M"))
            color = "white"
            t = hour * 100 + minute
            for r in conflict:
                if t in r:
                    color = "#ff3333"
            times.append(dict(id_num = id_num,
                            time = time,
                            color = color
                ))
    return times

def get_all_users(current_user):
    query = select([tbl_user])
    all_users = connectDB(query)
    users_list = []
    friends_list = []
    for user in all_users:
        user = User(user)
        if checkFriend(current_user.get_uid(), user.get_uid()):
            if current_user.get_uid() != user.get_uid():
                friends_list.append(user)
        else:
            users_list.append(user)
    return users_list, friends_list
