# Import Flask
from flask import Flask, render_template, request, json, redirect, url_for

from flask_login import LoginManager, UserMixin

# Import Time class for getting, parsing and formatting time
from time import strftime, strptime, localtime

from datetime import timedelta, date

# Import our package for functional requirements
from Actions import *

# Create global instance of the class 
application = Flask(__name__)

@application.route('/', methods = ['GET'])
def welcome():
    global current_user, logged_in
    if logged_in:
        eventsList = getEvents(current_user.get_uid())
        eventsList.sort()
        return render_template('home.html', 
                                current_user = current_user,
                                eventsList = eventsList,
                                strptime = strptime,
                                strftime = strftime)
    return render_template('welcome.html')

@application.route('/login/', methods=['GET', 'POST'])
def login():
    global logged_in, current_user
    if not logged_in:
        if request.method == 'POST':
            user_username = request.form['user_username']
            user_password = request.form['user_password']
            authenticated = checkLogin(user_username, user_password)
            if authenticated:
                logged_in = True
                current_user = getUser(user_username)
                return redirect(url_for('welcome'))
            else:
                return render_template('login.html', error = "Invalid Login")                    
        return render_template('login.html', error = None)
    return redirect('/')

@application.route('/signup/', methods=['GET', 'POST'])
def signup():
    global logged_in, current_user
    if not logged_in:
        if request.method == 'POST':
            userInfo = request.form
            user_username = request.form['user_username']
            success = createUser(userInfo)
            if success:
                logged_in = True
                current_user = getUser(user_username)
                return redirect(url_for('welcome'))
            else:
                return render_template('signup.html', error = 'Username taken')
        return render_template('signup.html', error = None)
    return redirect('/')

@application.route('/logout/', methods=['GET'])
def logout():
    global logged_in
    logged_in = False
    return redirect('/')

@application.route('/friends/', methods=['GET'])
def friends():
    if logged_in:
        userList, friendsList = get_all_users(current_user)
        return render_template('friends.html',
                                friendsList = friendsList,
                                userList = userList,
                                current_user = current_user)
    return redirect('/')


@application.route('/profile/', methods=['GET', 'POST'])
@application.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username = None):
    global current_user, logged_in
    if logged_in:
        if username == None:
            username = current_username.get_username();
        
        user = getUser(username)
        friendsList = getFriends(user.get_uid())
        eventsList = getEvents(user.get_uid())
        eventsList.sort()        
        if request.method == 'POST':
            if request.form['friend_status'] == 'friend':
                addFriend(current_user.get_uid(), user.get_uid())
                addFriend(user.get_uid(), current_user.get_uid())
            elif request.form['friend_status'] == 'unfriend':
                removeFriend(current_user.get_uid(), user.get_uid())
                removeFriend(user.get_uid(), current_user.get_uid())

        friend_status = checkFriend(current_user.get_uid(), user.get_uid())
        return render_template('profile.html',
                                friend_status = friend_status,
                                current_user = current_user,
                                user = user,
                                friendsList = friendsList,
                                eventsList = eventsList,
                                strftime = strftime,
                                strptime = strptime,)
    return redirect('/')

@application.route('/calendar/', methods=['GET', 'POST'])
def calendar():
    if logged_in:
        current_date = str(date.today())
        if request.method == 'POST':
            current_date = request.form.get('date', current_date)
        eventsList = getEvents(current_user.get_uid(), current_date)
        return render_template('calendar.html',
                                current_user = current_user,
                                current_date = current_date,
                                eventsList = eventsList,    
                                strptime = strptime,
                                strftime = strftime)
    return redirect('/')

@application.route('/compare/', methods=['GET', 'POST'])
def compare():
    if logged_in:
        current_date = str(date.today())
        friend_uid = current_user.get_uid()
        if request.method == 'POST':
            friend_uid = int(request.form["friend_uid"])
            current_date = request.form.get('date', current_date)
        friend = getUser(friend_uid)
        eventsList1 = getEvents(current_user.get_uid(), current_date)
        eventsList2 = getEvents(friend.get_uid(), current_date)
        times = compareSchedules(eventsList1 + eventsList2)
        
        return render_template('compare.html',
                                current_user = current_user,
                                current_date = current_date,
                                friend = friend,
                                eventsList1 = eventsList1,
                                eventsList2 = eventsList2,
                                times = times,
                                strftime = strftime,
                                strptime = strptime,
                                )
    return redirect('/')

@application.route('/new_event/', methods=['GET', 'POST'])
def new_event():
    global current_user, logged_in
    if logged_in:
        if request.method == 'POST':
            eventInfo = request.form
            success = createEvent(current_user.get_uid(), eventInfo)
            if success:
                return redirect('/')
        date = strftime("%Y-%m-%d", localtime())
        stime = strftime("%H:%M", localtime())
        etime = str((int(strftime("%H%M", localtime())) + 100) % 2400)
        etime = etime[:2] + ":" + etime[2:]
        return render_template('new_event.html', 
                                current_user = current_user,
                                date = date,
                                stime = stime,
                                etime = etime)
    return redirect('/')

@application.route('/event/<int:EID>', methods=['GET', 'POST'])
def event(EID):
    global current_user, logged_in
    if logged_in:
        event = getEvent(EID)
        if request.method == 'POST':
            return redirect('/event/edit/{}'.format(EID))
        return render_template('view_event.html',
                                current_user = current_user,
                                event = event,
                                strptime = strptime,
                                strftime = strftime)
    return redirect('/')

@application.route('/event/edit/<int:EID>', methods=['GET', 'POST'])
def edit_event(EID):
    global current_user, logged_in
    if logged_in:
        event = getEvent(EID)
        if request.method == 'POST':
            eventInfo = request.form
            success = editEvent(eventInfo, EID)
            if success:
                return redirect('/event/{}'.format(EID))
        return render_template('edit_event.html', 
                                current_user = current_user,
                                event = event)
    return redirect('/')

@application.route('/delete_event/', methods=['POST'])
def delete_event():
    global current_user, logged_in
    if logged_in:
        EID = request.form['EID']
        deleteEvent(EID)
    return redirect('/')

if __name__ == "__main__":
        app.debug = True
        application.run(port=5000)