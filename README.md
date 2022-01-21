# hospital_management_system
##  MVT Architecture
#### Django MVT Control Flow

![image](https://user-images.githubusercontent.com/59027621/150310955-f2f92325-b544-41ec-9136-ef215387fc3e.png)
![3](https://user-images.githubusercontent.com/59027621/150311461-da686970-7cb2-4e48-86e4-6439027d93ac.png)
![how does django work](https://user-images.githubusercontent.com/59027621/150310689-891deb72-2c9e-479c-bd31-ef2f45b83453.JPG)


#### The Model-View-Template (MVT) Architecture is a software design pattern for developing web applications.
- The Model is an interface for maintaining and managing data in the database in proper tables.
- The View interface executes the logic and interacts with the models.
- The Templates help to render the information received as a response from the views based on the request on the browser for user interaction.

#### How the application works?
![image](https://user-images.githubusercontent.com/59027621/150312551-d784e13c-2e96-4b0f-bf2d-1bf5296a0061.png)

- know more about the django request lifecycle [here](http://django-easy-tutorial.blogspot.com/2017/03/django-request-lifecycle.html?m=1)

# first video : create the project
## making a hms part 1

```python
py -m venv DjangoProject
DjangoProject\Scripts\activate.bat
py -m pip install Django
py -m django --version
```

## making a hms part 2

```python
cd DjangoProject
django-admin startproject hms
cd hms
py manage.py runserver
```
## stop the server
- ctrl+C

# create the app
## If a new cmd is open, then write down following to activate the virtual env

```python
DjangoProject\Scripts\activate.bat
cd DjangoProject
cd hms
py manage.py runserver
```
## making a hms part 3

```python
py manage.py startapp hospital
```

## we have an app now so we should tell our server to run the app with the project as well
- go to hms folder
- go to settings.py
- change the INSTALLED_APPS variable
- write down the app name at the last of this var **'hospital',**

# 2nd video : create a function in views.py and link it with urls.py

- Caution : don't name static and templates folder with other names 

```python
cd hospital
mkdir static templates
```

## what is views.py?

- we writes some python functions in this file which takes a web request and returns a web response.
- the response can be the html contents of a webpage, a redirect or a 404 error(not found).
- each view function takes a HTTP request as its first parameter
- go to the views.py write a 
```python
def homepage(request): 
    return render(request,'index.html') 
```
- render() is a shortcut function to return the given template
- go to the templates folder, create a file index.html
- go to the urls.py in the project folder
```python
from hospital.views import *
```
- write in the urlpatterns the following, we will give an empty url as homepage should be viewed at first
```python
path('',homepage,name='homepage'),
```

# 3rd video : manage the static files
- open the index.html and write ```{% load static %}```
- now in the stylesheets format the ```href="{% static 'bootstrap/css/bootstrap.min.css' %}"```
- similarly format the scripts ```src={% static 'js/Sidebar-Menu.js' %}```
- or background-image attr in style ```style="background-image: url(&quot;{% static 'img/star-sky.jpg' %}&quot;);"```

# 4th video : create a superuser and make groups for the user
- who is superuser?- the admin/administrator who can handle all the operations of the website
- in urls.py there is a path ```path('admin/', admin.site.urls),```
- Django gives an admin page for the superusers manually
```python
python manage.py migrate
```
- like tables in SQL, Django uses ORM(object relational model) in which we write models and we do not write any CRUD syntx instead we write them using python classes
- to apply models, we make migrations
- to create a new model ```python manage.py makemigrations```
- to apply, ```python manage.py migrate```

## create the superuser
```python
python manage.py createsuperuser
```
- give username, email, pass
- press y
- start the server and go to url "http://127.0.0.1:8000/admin"

## create users
- everyone who creates an account in the website is a user
- the users belong to Patient, Doctor, Admin groups
- add group : doctor, patient normally and save
- add group admin : give all permissions and save

# 5th video : create other urls
```python
def aboutpage(request): 
    return render(request,'about.html') 
```
- write in the urlpatterns the following, we will give an empty url as homepage should be viewed at first
```python
path('/about/',aboutpage,name='aboutpage'),
```
- go to the index.html
- change ```href="{% url 'aboutpage' %}"```
- what is happening here -> searches for the url named aboutpage in urls.py -> goes for the method given in url pattern which matched the name -> renders the html template written in that method
- create a navbar.html and copy the nav tag to that file so that you can load the navbar.html in every html template
- don't forget to write ```{% load static %}``` in navbar.html
- then include the navbar.html using ```{% include 'navbar.html' %}```

# 6th video : Signup and user registration
- go to views.py
```python
def createaccount(request):
    return render(request, 'createaccount.html')

# dont define it as login define it as login page
def loginpage(request):
    return render(request, 'login.html')
```
- go to urls.py and these in url patterns
```python
path('createaccount/', createaccount, name='createaccount'),
path('login/', loginpage, name='loginpage'),
```

- only a patient can create an account on his own. becoz he is a primary user for the website, but the doctors cannot create account on his own. 
- admins will create accounts for doctors so that other normal users cannot create accounts as doctors. the signup page is only for patients.
- As soon as the user hits the create account button of "submit" type, we should get the form data and save them in the database.
- for this, the method type of the form should be "POST".
- to protect the data from attack after submitting, we will use "{% csrf_token %}"
- every input tag must have a name attr
- to save the patient info we need to create patient model in models.py under the app directory


```python
class Patient(models.Model):
    # we will not save the password in Patient Model, so that the admins cannot view it.
    # make some columns for the models
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # primary key for this model
    password = models.CharField(max_length=16)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    birthdate = models.DateField()
    bloodgroup = models.CharField(max_length=5)

    # to show the patient name in patient group in panel
    def __str__(self):
        return self.name
```
- open the cmd
```python 
python manage.py makemigrations
python manage.py migrate
```
- go to admin.py
```python
from .models import *
admin.site.register(Patient)
```
- now check on admin url that the model Patient has come or not
- now go to the views.py file

```python
def createaccount(request):
    # initialize user
    user = "none"
    error = ""
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']
        
        try:
            if password == repeatpassword:
            # insert the values in the database
                Patient.objects.create(name=name, email=email,gender=gender,
                                       phonenumber=phonenumber,
                                       address=address,
                                       birthdate=birthdate,
                                       bloodgroup=bloodgroup)
                                       
                # we don't have any column in the database for passwords
                # django provides an authentication system  which consists of users,permissions, groups etc.
                # patient is also a user and he comes under the group patient
                # so the user who created an account, his details would be saved in the custom models and his authentication details will be stored in 'user'
                # for that we need to import user, groups
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                # admin cannot view the password of the patient because we have saved password in the USER Model
                
                # get the patient group 
                pat_group = Group.objects.get(name='Patient')
                # add the user to the patient group
                pat_group.user_set.add(user)
                # save the data in the user model
                user.save()
                error = 'no'
            else:
                error = 'yes'
        except Exception as e:
            #raise e
            error = 'yes'
    # make a dictionary and send the error to createaccount.html page by using it as a third parameter of render() function at the last
    d = {'error': error}
    # print(error)
    return render(request, 'createaccount.html', d)
    

# dont define it as login define it as login page
def loginpage(request):
    return render(request, 'login.html')
```
```python
from django.contrib.auth.models import User, Group
```

- now open the createaccount.html page and add this before the end of body tag
```html
{% if error == "no" %}
<script type="text/javascript">
    alert('Patient saved Sucessfully..........')
    window.location = ('{% url 'loginpage' %}')
</script>
{% endif %}
{% if error == "yes" %}
<script type="text/javascript">
    alert('something went wrong')
    window.location = ('{% url 'loginpage' %}')
</script>
{% endif %}
```
- use fake filler to fillup the createaccount.html and check whther it is working or not
- check whether the patient details are getting saved or not, go to http://localhost:8000/admin/hospital/patient
- see that the patient's name is being saved as we used this on patient model
```python
def __str__(self):
        return self.name
```

#### things to remember
- 1. Method type should be post
- 2. Every input tag must have a name attribute
- 3. There should a button with submit type
- 4. {% csrf_token %} should be mentioned inside the form tag

# 7th video : User login and logout
- first import 
```python
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
```
- the login method : the user enters input data for login, we get the data and match the user data with saved data in database
- for which model we need to search the user, we don't directly search the rows in the patient model and also we save the password in user model
- so the ans is user model
```python

def loginpage(request):
    error = ""
    # authenticate takes three parameters ; request, username, password
    if request.method == 'POST':
        # got the details from the login form
        u = request.POST['email']
        p = request.POST['password']
        # print(u)
        # print(p)
        # this statement searches for the rows in the user model and saves them in the variable user
        user = authenticate(request, username=u, password=p)
        try:
            # confirm that the user is present or not
            if user is not None:
                error = "no"
                # login with the user
                login(request, user)
                
                # according to the group of user, patient/doctor/receptionist we will redirect them to the required pages
                # we are getting the group name of the user from the list
                g = request.user.groups.all()[0].name
                if g == 'Patient':
                    d = {'error': error}
                    return HttpResponse("Patient Logged in Successfully")
                    # return render(request, 'patienthome.html', d)
        # if there is no user then prints error
        except Exception as e:
            error = "yes"
            print(e)
            # raise e
    return render(request, 'login.html')
```
- now go to the login page
- login and test

### logout
- in views.py
- uncomment the render function() in loginpage method

```python
def Logout(request):
    logout(request)
    return redirect('loginpage')
```
- in urls.py add this to urlpattern
```python 
path('logout/', Logout, name='logout'),
```
# 8th video : User profile
- in views.py
```python
def Home(request):
    # what if an unknown user is redirected to this url or he writes in the browser /home/ url, how do we restrict him from accessing this page?
    # if not a known user or a user who is not logged in but trying to access the home page then redirect him to login page
    if not request.user.is_active:
        return redirect('loginpage')

    # there is a homepage for every user, but we cannot create a view for every user
    # so we will redirect them to respective homepage using their groups
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        return render(request, 'patienthome.html')

```
- in urls.py
```
 path('home/', Home, name='home'),
```
- go to patienthome.html page and write this before </body> tag
```html
    {% if error == "no" %}
    <script type="text/javascript">
        window.location = ('{% url 'home' %}')
    </script>
    {% endif %}
    {% if error == "yes" %}
    <script type="text/javascript">
        alert('Invalid Credentials')
        window.location = ('{% url 'loginpage' %}')
    </script>
    {% endif %}
```
- place the url in href in navbar tag ``{% url 'home' %}``
- in views.py
```python
def profile(request):
    # this statement is common whenever an user is not logged in
    if not request.user.is_active:
        return redirect('loginpage')

    # there is a homepage for every user, but we cannot create a view for every user
    # so we will redirect them to respective homepage using their groups
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        # email is the primary key here so it is used to filter all the patients
        # request.user gives the username
        patient_details = Patient.objects.all().filter(email=request.user)  
        d = {'patient_details': patient_details}
        return render(request, 'patientprofile.html', d)
```
- in urls.py
```python
path('profile/', profile, name='profile'),
```
- in patientprofile.html add ``{% for d in patient_details %}`` before form tag opening and add ``{% endfor %}`` after form tag closing 
- add readonly to every input tag
- add value ="{{d.name}}" 
- test after login in server

# 9th video : create the doctor model and make appointments
- in models.py
```python
class Doctor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    birthdate = models.DateField()
    bloodgroup = models.CharField(max_length=5)
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return self.name
        
class Appointment(models.Model):
    doctorname = models.CharField(max_length=50)
    doctoremail = models.EmailField(max_length=50)
    patientname = models.CharField(max_length=50)
    patientemail = models.EmailField(max_length=50)
    appointmentdate = models.DateField(max_length=10)
    appointmenttime = models.TimeField(max_length=10)
    symptoms = models.CharField(max_length=100)
    # which appointments are done, which are pending that status
    status = models.BooleanField()
    prescription = models.CharField(max_length=200)

    def __str__(self):
        return self.patientname+" you have appointment with "+self.doctorname
```
- in cmd
```console
python manage.py makemigrations
python manage.py migrate
```
- go to admin.py
```python
from .models import *
admin.site.register(Doctor)
admin.site.register(Appointment)
```
- now lets make a doctor through admin panel
- go to admin panel -> hospital -> doctors -> add -> save
- go to authentication and authorization -> users -> add user -> save
- add him to the group doctor
- save
- now go to views.py
```python
def MakeAppointments(request):
    error = ""
    if not request.user.is_active:
        return redirect('loginpage')
    # get all the registered doctors
    alldoctors = Doctor.objects.all()
    d = {'alldoctors': alldoctors}
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        if request.method == 'POST':
            temp = request.POST['doctoremail']
            doctoremail = temp.split()[0]
            doctorname = temp.split()[1]
            patientname = request.POST['patientname']
            patientemail = request.POST['patientemail']
            appointmentdate = request.POST['appointmentdate']
            appointmenttime = request.POST['appointmenttime']
            symptoms = request.POST['symptoms']
            try:
                Appointment.objects.create(doctorname=doctorname, doctoremail=doctoremail, patientname=patientname, patientemail=patientemail,
                                           appointmentdate=appointmentdate, appointmenttime=appointmenttime, symptoms=symptoms, status=True, prescription="")
                error = "no"
            except:
                error = "yes"
            e = {"error": error}
            return render(request, 'patientmakeappointments.html', e)
        elif request.method == 'GET':
            return render(request, 'patientmakeappointments.html', d)
```
- now go to the urls.py
```python
path('makeappointments/', MakeAppointments, name='makeappointments'),
```
- go to patientmakeappointments.html page add for loop to make a list of registered doctors
```html 
    <select class="form-control" name="doctoremail">
        {% for d in alldoctors %}
        <option value="{{d.email}} {{d.name}}">{{d.name}}---->{{d.specialization}}</option>
        {% endfor %}
    </select>
```
- and also add
```html
value="{{user.first_name}}"
```
- the user here is the logged in user , now patient
- add this before the body tag ends
```html
    {% if error == "no" %}
    <script type="text/javascript">
        alert('appointment booked successfully')
        window.location = ('{% url 'makeappointments' %}')
    </script>
    {% endif %}
    {% if error == "yes" %}
    <script type="text/javascript">
        alert('something went wrong')
    </script>
    {% endif %}
```
- and now try booking an appointment and check whether that appears in the admin panel or not

# 10th video : view appointments for patients
- in views.py
```python
from django.utils import timezone



def viewappointments(request):
    if not request.user.is_active:
        return redirect('loginpage')
    # print(request.user)
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        # appointmentdate__gte -> greater than
       
        upcomming_appointments = Appointment.objects.filter(patientemail = request.user, appointmentdate__gte = timezone.now(), status = True).order_by('appointmentdate')
        #print("Upcomming Appointment",upcomming_appointments)
        # appointmentdate__lt -> less than
        # -appointmentdate -> to show the appointments in decreasing order, we write minus appointmentdate
        # we want to show last appointmentdate above all other, so - is given before apppointmentdate
        previous_appointments = Appointment.objects.filter(patientemail = request.user, appointmentdate__lt = timezone.now()).order_by('-appointmentdate') |                     
                                Appointment.objects.filter(patientemail = request.user, status = False).order_by('-appointmentdate')
        #print("Previous Appointment",previous_appointments)
        d = {"upcomming_appointments": upcomming_appointments,
             "previous_appointments": previous_appointments}
        return render(request, 'patientviewappointments.html', d)
```
- in urls.py
```python
 path('viewappointments/', viewappointments, name='viewappointments'),
```
- in patientviewappointments.html
- add this before ul tag opening in page-content-wrapper ```{% for i in upcomming_appointments %}```
- add this in li tag ```{{ i.patientname }} appointment with {{ i.doctorname }} on {{i.appointmentdate}}```
- end the forloop after ul tag closing ``{% endfor %}``
- again do the same for previous appointments 
- now login and test on the server

### end of our project tutorial

