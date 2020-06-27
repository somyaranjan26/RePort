from django.shortcuts import render
from django.contrib import auth     # for handeling user session
import pyrebase

from datetime import datetime, timezone
import time
import pytz

config = {
    # paste your firebase credentials here.
}

firebase = pyrebase.initialize_app(config);    # configuring firebase using pyrebase
authentication = firebase.auth();              # getting user authentication data from firebase
database = firebase.database();

def index(request):
    return render(request, "index.html")       # Landing Page


def logIn(request):
    return render(request, "logIn.html")       # LogIn page 


def signIn(request):
    return render(request, "signUp.html")


def newUser(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    # try:
    user = authentication.create_user_with_email_and_password(email, password)  # Adding data to 
    # except:
    #     message = "Getting some issue with your credential, Please try again with any credential"   # firebase
    #     para = {"message": message}
    #     return render(request, 'signUp.html', para)
                                                                           
    uid = user['localId']                       # getting user's local id
    data = {"name": name, "status": 1}

    idtoken = user['idToken']

    database.child("users").child(uid).child("details").set(data, idtoken)
    return render(request, "logIn.html", data)
 

def home(request):
    email = request.POST.get('email')          # getting email id from the HTML form 
    password = request.POST.get('password')    # getting password id from the HTML form 

    try:
        user = authentication.sign_in_with_email_and_password(email, password)  # checking log In creadentials 
    except:                                                           
        para = {"message": "❌Something went wrong 👀, Please try again!"}  # if creadentials are 
        return render(request, "logIn.html", para)         # incorrect, redirect to sign in page

    request.session['uId'] = str(user['idToken'])
    idtoken = request.session['uId']

    uId = user['localId']
    userName = database.child('users').child(uId).child('details').child('name').get(idtoken).val()

    para = { "name": userName}
    return render(request, "Home.html", para)


def logOut(request):
    try:
        del request.session['uId']           # It will delete the session
    except KeyError:
        pass                                # if session were not there and user will logout, 
    return render(request, "index.html")    # then it simply render Landing page.


def addTask(request):
    taskTitle = request.POST.get("taskTitle")
    aboutTask = request.POST.get("aboutTask")

    tz = pytz.timezone('Asia/Kolkata')                     # Specify the timezone
    time_now = datetime.now(timezone.utc).astimezone(tz)   # Get current UTC time and 
                                                           # convert it into specified time zone 
    millis = int(time.mktime(time_now.timetuple()))        # convert the time into millisecond
    
    try:
        idtoken = request.session['uId']                    # fetching user details
        uId = authentication.get_account_info(idtoken)      # getting user's Local ID
        uId = uId['users']
        uId = uId[0]
        uId = uId['localId']

        data = {
            "taskTitle": taskTitle,
            "aboutTask": aboutTask 
        }
        if database.child("users").child(uId).child("reports").child(millis).set(data, idtoken):
            userName = database.child('users').child(uId).child('details').child('name').get(idtoken).val()

            para = { "name": userName, "message": "Your task successfully added 👍"}
            return render(request, "home.html", para)
        else:
            para = {"message": "👀 Something went wrong, Please Log In again"}
            return render(request, "logIn.html", para)            
    
    except KeyError:
        para = {"message": "👀 User is logged out, Please Log In again!"}  # if creadentials are 
        return render(request, "logIn.html", para)         # incorrect, redirect to sign in page


def viewTaskList(request):
    idtoken = request.session['uId']                    # fetching user details
    uId = authentication.get_account_info(idtoken)      # getting user's Local ID
    uId = uId['users']
    uId = uId[0]
    uId = uId['localId']

    try:
        timestamps = database.child("users").child(uId).child("reports").shallow().get(idtoken).val()
        timeList = []
    
        taskCount = 0
        for i in timestamps:
            taskCount = taskCount + 1
            timeList.append(i)
        
        timeList.sort(reverse=True)

        taskTitle = []
        aboutTask = []
        for i in timeList:
            taskName = database.child("users").child(uId).child("reports").child(i).child("taskTitle").get(idtoken).val() 
            TaskDesc = database.child("users").child(uId).child("reports").child(i).child("aboutTask").get(idtoken).val()
            taskTitle.append(taskName)
            aboutTask.append(TaskDesc)
        
        taskDate = []
        for i in timeList:
            i = float(i)                                                        # typecast string to float 
            date = datetime.fromtimestamp(i).strftime("%H:%M %p, %d-%m-%Y")     # extracting date and time from float
            taskDate.append(date)
        
        data = zip(timeList, taskDate, taskTitle, aboutTask)
        userName = database.child('users').child(uId).child('details').child('name').get(idtoken).val()
    
        para = {"name": userName, "data": data, "count": taskCount}
        return render(request, "viewTaskList.html", para)
    
    except:
        userName = database.child('users').child(uId).child('details').child('name').get(idtoken).val()
        para = {"name": userName, "message": "👀 Seems your Task List 📝 is Empty 📂"} 
        return render(request, "home.html", para)        
    
    

def addNewTask(request):
    try:
        idtoken = request.session['uId']                    # fetching user details
        uId = authentication.get_account_info(idtoken)      # getting user's Local ID
        uId = uId['users']
        uId = uId[0]
        uId = uId['localId']
        userName = database.child('users').child(uId).child('details').child('name').get(idtoken).val()

        para = { "name": userName}
        return render(request, "home.html", para)
    except KeyError:
        para = {"message": "👀 User is logged out, Please Log In again!"}  # if creadentials are 
        return render(request, "logIn.html", para)         # incorrect, redirect to sign in page


def deleteTask(request):
    time = request.GET.get("time")
    
    try:
        idtoken = request.session['uId']                    # fetching user details
        uId = authentication.get_account_info(idtoken)      # getting user's Local ID
        uId = uId['users']
        uId = uId[0]
        uId = uId['localId']

        database.child("users").child(uId).child("reports").child(time).remove(idtoken)
        
        timestamps = database.child("users").child(uId).child("reports").shallow().get(idtoken).val()
        timeList = []
        
        if timestamps:
            taskCount = 0
            for i in timestamps:
                taskCount = taskCount + 1
                timeList.append(i)
            
            timeList.sort(reverse=True)

            taskTitle = []
            aboutTask = []
            for i in timeList:
                taskName = database.child("users").child(uId).child("reports").child(i).child("taskTitle").get(idtoken).val() 
                TaskDesc = database.child("users").child(uId).child("reports").child(i).child("aboutTask").get(idtoken).val()
                taskTitle.append(taskName)
                aboutTask.append(TaskDesc)
            
            taskDate = []
            for i in timeList:
                i = float(i)                                                        # typecast string to float 
                date = datetime.fromtimestamp(i).strftime("%H:%M %p, %d-%m-%Y")     # extracting date and time from float
                taskDate.append(date)
            
            data = zip(timeList, taskDate, taskTitle, aboutTask)
            userName = database.child('users').child(uId).child('details').child('name').get(idtoken).val()
        
            para = {"name": userName, "data": data, "count": taskCount}
            return render(request, "viewTaskList.html", para)
        else:
            userName = database.child('users').child(uId).child('details').child('name').get(idtoken).val()
            para = {"name": userName, "message": "👀 Seems your Task List 📝 is Empty 📂"} 
            return render(request, "home.html", para)

    except KeyError:
        para = {"message": "👀 User is logged out, Please Log In again!"}  # if creadentials are 
        return render(request, "logIn.html", para)         # incorrect, redirect to sign in page
