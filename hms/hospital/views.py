from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.


def homepage(request):
    return render(request, 'index.html')


def aboutpage(request):
    return render(request, 'about.html')


def createaccount(request):
    # initialize user
    user = "none"
    error = ""
    if request.method == 'POST':
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
                Patient.objects.create(name=name, email=email,
                                       gender=gender,
                                       phonenumber=phonenumber,
                                       address=address,
                                       birthdate=birthdate,
                                       bloodgroup=bloodgroup)

                # we don't have any column in the database for passwords
                # django provides an authentication system  which consists of users,permissions, groups etc.
                # patient is also a user and he comes under the group patient
                # so the user who created an account, his details would be saved in the custom models and his authentication details will be stored in 'user'
                # for that we need to import user, groups
                user = User.objects.create_user(
                    first_name=name, email=email, password=password, username=email)
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

# dont define it as login define it as login page


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
                    # return HttpResponse("Patient Logged in Successfully")
                    return render(request, 'patienthome.html', d)
        # if there is no user then prints error
        except Exception as e:
            error = "yes"
            print(e)
            # raise e
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('loginpage')

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
        previous_appointments = Appointment.objects.filter(patientemail = request.user, appointmentdate__lt = timezone.now()).order_by('-appointmentdate')| Appointment.objects.filter(patientemail = request.user, status = False).order_by('-appointmentdate')
        #print("Previous Appointment",previous_appointments)
        d = {"upcomming_appointments": upcomming_appointments,"previous_appointments": previous_appointments}
        return render(request, 'patientviewappointments.html', d)
