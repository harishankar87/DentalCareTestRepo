from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Doctor, Patient, Prescription, passwordHasher, emailHasher, Appointment
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .forms import AppointmentSet, AppointmentSetForm
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from .Whatsapptestfile import whatsappApi

# from Whatsapptestfile import psutil

# Create your views here.
def index(request):
    """ Function for displaying main page of website. """
    
    # Editing response headers so as to ignore cached versions of pages
    response = render(request,"HealthCentre/index.html")
    return responseHeadersModifier(response)

def register(request):
    """ Function for registering a student into the portal. """

    # If the user wants the page to get displayed

    if request.method == "GET":
        # Editing response headers so as to ignore cached versions of pages

        response =  render(request,"HealthCentre/registrationPortal.html")

        return responseHeadersModifier(response)
    
    # If the user wants to submit his/her information

    elif request.method == "POST":
        # Extracting the user information from the post request
        userFirstName = request.POST["userFirstNam"]
        userLastName = request.POST["userLastName"]
        userEmail = request.POST["userEmail"]
        userRollNo = request.POST["userRollNo"]
        userAddress = request.POST["userAddress"]
        userContactNo = request.POST["userContactNo"]
        userPassword = request.POST["userPassword"]
        userConfirmPassword = request.POST["userConfirmPassword"]

        # If both the passwords match
        if userPassword == userConfirmPassword:

            name = userFirstName + " " + userLastName

            # Encrypting password to store inside database
            passwordHash = passwordHasher(userPassword)

            # Encrypting email to store inside database
            emailHash = emailHasher(userEmail)

            # handleSubmit(request)
            # def handleSubmit(request):
            
            
            # Creating a patient object and saving insdie the database if patient is selected 
            userType = request.POST['userType']
            if userType == 'patient':
                # patient = Patient(rollNumber=request.POST['rollNumber'])
                patient = Patient(name = name,rollNumber = userRollNo, email = userEmail, passwordHash = passwordHash, address = userAddress, contactNumber = userContactNo, emailHash = emailHash )
                patient.save()
                    
            # Creating a patient object and saving insdie the database if patient is selected
            elif userType == 'doctor':
                doctor = Doctor(name = name, specialization= userRollNo, email = userEmail, passwordHash = passwordHash, address = userAddress, contactNumber = userContactNo, emailHash = emailHash)
                doctor.save()


            
            

            # Creating a patient object and saving insdie the database
            # patient = Patient(name = name,rollNumber = userRollNo, email = userEmail, passwordHash = passwordHash, address = userAddress, contactNumber = userContactNo, emailHash = emailHash )
            # patient.save()

            # Storing success message in the context variable
            context = {
                "message":"User Registration Successful. Please Login."
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request, "HealthCentre/registrationPortal.html",context)
            return responseHeadersModifier(response)

        # If the passwords given don't match
        else:
            # Storing failure message in the context variable
            context = {
                "message":"Passwords do not match.Please register again."
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request,"HealthCentre/registrationPortal.html",context)
            return responseHeadersModifier(response)

    # For any other method of request, sending back the registration page.
    else:

        # Editing response headers so as to ignore cached versions of pages
        response = render(request,"HealthCentre/registrationPortal.html")
        return responseHeadersModifier(response)


def doctors(request):
    """Function to send information about the doctors available to the user. """

    # Storing doctors available in the context variable
    context = {
        "doctors" : Doctor.objects.all()
    }

    # Editing response headers so as to ignore cached versions of pages
    response = render(request,"HealthCentre/doctors.html",context)
    return responseHeadersModifier(response)


def login(request):
    """ Function for logging in the user. """

    # Calling session variables checker
    request = requestSessionInitializedChecker(request)

    # If the request method is post
    if request.method == "GET":
        try:

            # If the user is already logged in inside of his sessions, and is a doctor, then no authentication required
            if request.session['isLoggedIn'] and request.session['isDoctor']:
                # Accessing the doctor user and all his/her records
                doctor = Doctor.objects.get(emailHash = request.session['userEmail'])
                records = doctor.doctorRecords.all()
                # Getting the count of the new prescriptions pending
                numberNewPendingPrescriptions = doctor.doctorRecords.aggregate(newnewPendingPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = False) ) ))['newnewPendingPrescriptions']
                # Storing the same inside the session variables
                request.session['numberNewPrescriptions'] = numberNewPendingPrescriptions

                # Storing the required information inside the context variable
                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp'),
                    "prescriptions" : Prescription.objects.all().order_by('timestamp')
                }
                
                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"HealthCentre/prescriptionPortal.html", context)
                return responseHeadersModifier(response)
            
            # If the user is already logged in inside of his sessions, and is a patient, then no authentication required
            elif request.session['isLoggedIn'] and (not request.session['isDoctor']):

                # Accessing the patient user and all his/her records
                patient = Patient.objects.get(emailHash = request.session['userEmail'])
                records = patient.patientRecords.all()

                # Getting the count of the new prescriptions pending
                numberNewPrescriptions = patient.patientRecords.aggregate(newCompletedPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = True) ) ) )['newCompletedPrescriptions']

                # Storing the same inside the session variables
                request.session['numberNewPrescriptions'] = numberNewPrescriptions

                # Updating the completed records
                for record in records:
                    if record.isCompleted:
                        record.isNew = False
                        record.save()

                # Storing the required information inside the context variable
                context = {
                    "message" : "Successfully Logged In.",
                    "isAuthenticated" : True,
                    "user": records.order_by('-timestamp')
                    }

                # Editing response headers so as to ignore cached versions of pages
                # response = render(request,"HealthCentre/prescriptionPortal.html")
                response = render(request,"HealthCentre/userPatientProfilePortal.html", context)
                return responseHeadersModifier(response)

            else:
                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"HealthCentre/loginPortal.html")
                return responseHeadersModifier(response)

        # If any error occurs, sending back a new blank page
        except:

            # Editing response headers so as to ignore cached versions of pages
            response = render(request,"HealthCentre/loginPortal.html")
            return responseHeadersModifier(response)

    # If the request method is post
    elif request.method == "POST":

        # Extracting the user information from the post request
        userName = request.POST["useremail"]
        userPassword = request.POST["userpassword"]

        # If such a patient exists
        try:
            patient = Patient.objects.get(email = userName)

            # Storing required session information
            request.session['isDoctor'] = False

        # Otherwise trying if a doctor exists
        except Patient.DoesNotExist:
            try:
                doctor = Doctor.objects.get(email = userName)

                # Storing required session information
                request.session['isDoctor'] = True     

            # If no such doctor or patient exists
            except Doctor.DoesNotExist:

                # Storing message inside context variable
                context = {
                    "message":"User does not exist.Please register first."
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"HealthCentre/loginPortal.html", context)
                return responseHeadersModifier(response)

        # Getting the hash of user inputted password
        passwordHash = passwordHasher(userPassword)

        # If the logged in user is a doctor
        if request.session['isDoctor']:
            
            # Accessing all records of doctor
            records = doctor.doctorRecords.all()

            # Getting the count of new prescriptions
            numberNewPendingPrescriptions = doctor.doctorRecords.aggregate(newPendingPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = False) ) ))['newPendingPrescriptions']

            # Storing the same inside request variable
            request.session['numberNewPrescriptions'] = numberNewPendingPrescriptions

            # If the inputted hash and the original user password hash match
            if passwordHash == doctor.passwordHash:

                # Storing required information in session variable of request
                request.session['isLoggedIn'] = True
                request.session['userEmail'] = doctor.emailHash
                request.session['Name'] = doctor.name

                # Redirecting to avoid form resubmission
                # Redirecting to home page
                # Editing response headers so as to ignore cached versions of pages
                # response = render(request,"HealthCentre/userDoctorProfilePortal.html")
                # response = HttpResponseRedirect(reverse('onlineprescription'))
                # response = render(request,"HealthCentre/prescriptionPortal.html")
                response = HttpResponseRedirect(reverse('index'))
                return responseHeadersModifier(response)

            # Else if the password inputted is worng and doesn't match
            else:

                # Storing message inside context variable
                context = {
                    "message":"Invalid Credentials.Please Try Again."
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"HealthCentre/loginPortal.html", context)
                return responseHeadersModifier(response)

        # Otherwise if the user is a patient
        else:

            # Accessing all records of patient
            records = patient.patientRecords.all()

            # Getting the count of new prescriptions
            numberNewPrescriptions = patient.patientRecords.aggregate(newCompletedPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = True) ) ))['newCompletedPrescriptions']

            # Storing the same inside request variable
            request.session['numberNewPrescriptions'] = numberNewPrescriptions

            # Updating the completed records
            for record in records:
                if record.isCompleted :
                    record.isNew = False
                    record.save()

            # If the inputted hash and the original user password hash match
            if passwordHash == patient.passwordHash:

                # Storing required information in session variable of request
                request.session['isLoggedIn'] = True
                request.session['userEmail'] = patient.emailHash
                request.session['Name'] = patient.name
                request.session['isDoctor'] = False

                # Redirecting to avoid form resubmission
                # Redirecting to home page
                # Editing response headers so as to ignore cached versions of pages
                # response = render(request,"HealthCentre/userPatientProfilePortal.html")
                # response = render(request, "HealthCentre/prescriptionportal.html")
                # response = HttpResponseRedirect(reverse('onlineprescription'))
                response = HttpResponseRedirect(reverse('index'))
                return responseHeadersModifier(response)

            # Else if the password inputted is worng and doesn't match
            else:

                # Storing message inside context variable
                context = {
                    "message":"Invalid Credentials.Please Try Again."
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request,"HealthCentre/loginPortal.html", context)
                return responseHeadersModifier(response)
    # For any other method of access, returning a new blank login page
    else:
        response = render(request,"HealthCentre/loginPortal.html")
        return responseHeadersModifier(response)

def emergency(request):
    """ Funtion for emergency situations, for requesting an ambulance."""

    # If the request method is get
    if request.method == "GET":

        # Editing response headers so as to ignore cached versions of pages
        response = render(request,"HealthCentre/emergencyPortal.html")
        return responseHeadersModifier(response)

    # If the request method is post and the user is submitting information
    elif request.method == "POST":

        # Extracting the emergency location from the post request
        emergencyLocation = request.POST['emergencyLocation']

        # Giving emergency message to server, can also be connected to IOT devices for alarms
        # If the emergency location text is not an empty string
        if emergencyLocation != "":

            # Printing information and notifying inside of server terminal
            print("------------------------------------------------------------------------")
            print("\n\nEMERGENCY !! AMBULANCE REQUIRED AT " + emergencyLocation + " !!\n\n")
            print("------------------------------------------------------------------------")

            # Storing information inside of context variable
            context = {
                "message" : "Ambulance reaching " + emergencyLocation + " in 2 minutes."
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request, "HealthCentre/emergencyPortal.html", context)
            return responseHeadersModifier(response)

        # Else if the emergency location is an empty string
        else:

            # Storing message inside context variable
            context = {
                "message" : "No location entered.Invalid input."
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request, "HealthCentre/emergencyPortal.html", context)
            return responseHeadersModifier(response)

    # For any other method of access, returning a new blank emergency page
    else:

        # Editing response headers so as to ignore cached versions of pages
        response = render(request,"HealthCentre/emergencyPortal.html")
        return responseHeadersModifier(response)

def logout(request):
    """Function to log out the user."""
    # Erasing all the information of the session variables if user is logged out
    request.session['isDoctor'] = ""
    request.session['isLoggedIn'] = False
    request.session['userEmail'] = ""
    request.session['Name'] = ""
    request.session['numberNewPrescriptions'] = ""

    # Redirecting to avoid form resubmission
    # Redirecting to home page
    # Editing response headers so as to ignore cached versions of pages
    response = HttpResponseRedirect(reverse('login'))
    return responseHeadersModifier(response)

def contactus(request):
    """Function to display contact information."""

    # Editing response headers so as to ignore cached versions of pages
    response = render(request, "HealthCentre/contactus.html")
    return responseHeadersModifier(response)


def doctorappointmentsfalse(request):
    if request.method == 'GET':
        # request.session['goToAppointmentsPage'] = True
        request.session['createNewAppointment'] = True
        if request.session['isLoggedIn'] and request.session['isDoctor'] and request.session['createNewAppointment']:
            # Accessing the doctor user and all his/her records
            # request.session['CreatenewAppointment'] = False
            doctor = Doctor.objects.get(emailHash = request.session['userEmail'])
            records = doctor.doctorRecords.all()
            # Getting the count of the new prescriptions pending
            numberNewPendingPrescriptions = doctor.doctorRecords.aggregate(newnewPendingPrescriptions = Count('pk', filter =( Q(isNew = True) & Q(isCompleted = False) ) ))['newnewPendingPrescriptions']

            # Storing the same inside the session variables
            request.session['numberNewPrescriptions'] = numberNewPendingPrescriptions

            # Storing the required information inside the context variable
            context = {
                "message" : "Successfully Logged In.",
                "isAuthenticated" : True,
                "user": records.order_by('-timestamp'),
                "Appointments" : Appointment.objects.all().order_by('time')
            }
            response = render(request,"HealthCentre/appointmentsPortal.html", context)
            return responseHeadersModifier(response)
        
def doctorappointments(request):
    if request.method == 'GET':
        request.session['goToAppointmentsPage'] = True
        # request.session['createNewAppointment'] = True
        form = AppointmentSetForm()
        model = Appointment()
        # form = AppointmentForm(request.POST or None)
        hour = range(00, 24)
        minute = range(00, 60)
        date = range(1, 32)
        month = range(1, 13)
        year = datetime.now().year
        
        context = {'form': form, 
                    'model': model,
                    'hours': hour,
                    'dates' : date,
                    'months' : month,
                    'years' : year,
                    'minutes': minute,
                    "patients" : Patient.objects.all().order_by('id'),
                    "prescPatients" : Prescription.objects.all().order_by('id')
                    }
        response = render(request, 'HealthCentre/NewAppointment.html', context)
        return responseHeadersModifier(response)
    if request.method == 'POST':
        if request.session['goToAppointmentsPage']:
            if request.POST['selectedPatient'] == "":
                appointmentPatient = request.POST['PatientNameForAppointment']
                # patient = Patient.objects.create(name=prescpatient)
            else:
                appointmentPatient = request.POST['selectedPatient']
                # prescpatient = request.POST['selectedPatient']
                # patient_id = request.POST['selectedPatient'] 
                # patient = Patient.objects.get(name=patient_id)
            appointmentTime = request.POST['EnterTimeHour'] + request.POST['EnterTimeMinute']
            datetimeObject = datetime.strptime(appointmentTime, "%H%M")
            appointmentDate = request.POST['EnterDate'] + request.POST['EnterDateMonth']
            dateobject = datetime.strptime(appointmentDate, "%m%d")
            appointmentNotes = request.POST['AppointmentDescription']
            appointmentDoctor = request.session['Name']
            appointmentSubject = "subject"
            appointment = Appointment(time = datetimeObject, date = dateobject, subject = appointmentSubject, notes = appointmentNotes,
                                        appointmentpatient = appointmentPatient, appointmentdoctor = appointmentDoctor)
            appointment.save()
        response = render(request, 'HealthCentre/appointmentsPortal.html')
        return responseHeadersModifier(response)
     
def doctorprofile(request):
     if request.method == 'GET':
        
        request.session['writeNewPrescription'] = True
        
        context = {
                    "patients" : Patient.objects.all().order_by('id'),
                    "prescPatients" : Prescription.objects.all().order_by('id')
                    
                    }
        response = render(request, "HealthCentre/NewPrescription.html", context)
        return responseHeadersModifier(response)

     if request.method == 'POST':
         if request.session['writeNewPrescription']:
            if request.POST['selectedPatient'] == "":
                prescpatient = request.POST['PatientName']
                patient = Patient.objects.create(name=prescpatient)
            else:
                prescpatient = request.POST['selectedPatient']
                patient_id = request.POST['selectedPatient'] 
                patient = Patient.objects.get(name=patient_id)

            symptoms = request.POST["symptoms"]
            if request.session['isLoggedIn'] and request.session['isDoctor']:
                prescdoctor = request.session['Name']
                # doctor = Doctor.objects.get(id=1)
                doctor_id = request.session['Name']
                doctor = Doctor.objects.get(name=doctor_id)
                # patient_id = request.POST['selectedPatient'] 
                # patient = Patient.objects.get(name=patient_id)
                prescriptiontext = request.POST['prescription']
                prescription = Prescription(prescribingDoctor = prescdoctor, prescribingPatient = prescpatient ,doctor = doctor, patient= patient, symptoms = symptoms, prescriptionText = prescriptiontext)
                prescription.save()
            context = {
                    "prescriptions" : Prescription.objects.all().order_by('timestamp')
                }
         response = render(request, "HealthCentre/prescriptionportal.html", context)
         return responseHeadersModifier(response)

def onlineprescription(request):
    """Function to submit online prescription request to doctor."""

    # Calling session variables checker
    request = requestSessionInitializedChecker(request)

    # If the request method is get
    if request.method == "GET":

        # If the user is logged in
        if request.session['isLoggedIn']:

            # Portal only for patient prescription request submission, not for doctors
            if request.session['isDoctor']:

                # Storing message inside context variable
                # context = {
                #         "message":"Only for patients."
                # }

                # Editing response headers so as to ignore cached versions of pages
                # response = render(request, "HealthCentre/prescriptionPortal.html", context)
                response = render(request, "HealthCentre/userDoctorProfilePortal.html")
                return responseHeadersModifier(response)

            # If the user is a patient
            else:

                # Storing available doctors inside context variable
                context = {
                    "doctors" : Doctor.objects.all().order_by('specialization')
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request, "HealthCentre/prescriptionPortal.html", context)
                return responseHeadersModifier(response)

        # If the user is not logged in
        else:

            # Storing message inside context variable
            context = {
                    "message":"Please Login First."
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request, "HealthCentre/prescriptionPortal.html", context)
            return responseHeadersModifier(response)

    # If the user is posting the prescription request
    elif request.method == "POST":

        # Accepting only if the user is logged in
        if request.session['isLoggedIn']:

            # If the prescription is being submitted back by a doctor
            if request.session['isDoctor']:

                # Extracting information from post request
                prescriptionText = request.POST['prescription']

                # Updating the prescription and saving it
                prescription = Prescription.objects.get(pk = request.POST['prescriptionID'])
                prescription.prescriptionText = prescriptionText
                prescription.isCompleted = True
                prescription.isNew = True
                prescription.save()

                # Getting the records of the doctor
                records = Doctor.objects.get(emailHash = request.session['userEmail']).doctorRecords.all()

                # Storing required information inside context variable
                context = {
                    "user" : records,
                    "successPrescriptionMessage" : "Prescription Successfully Submitted."
                }

                # Editing response headers so as to ignore cached versions of pages
                response = render(request, "HealthCentre/userDoctorProfilePortal.html", context)
                return responseHeadersModifier(response)

            # Else if the patient is submitting prescription request
            else:

                # Extracting information from post request and getting the corresponding doctor
                doctor = Doctor.objects.get(pk = request.POST["doctor"])
                symptoms = request.POST["symptoms"]

                # Saving the prescription under the concerned doctor
                prescription = Prescription(doctor = doctor, patient = Patient.objects.get(emailHash = request.session['userEmail']), symptoms = symptoms)
                prescription.save()

                # Storing information inside context variable
                context = {
                    "successPrescriptionMessage" : "Prescription Successfully Requested.",
                    "doctors"  : Doctor.objects.all().order_by('specialization')
                }

                # Editing response headers so as to ignore cached versions of pages
                # response = render(request, "HealthCentre/userDoctorProfilePortal.html", context)
                response = render(request, "HealthCentre/prescriptionPortal.html", context)
                return responseHeadersModifier(response)

        # Else if the user is not logged in
        else:

            # Storing information inside context variable
            context = {
                    "successPrescriptionMessage":"Please Login First.",
            }

            # Editing response headers so as to ignore cached versions of pages
            response = render(request, "HealthCentre/loginPortal.html", context)
            return responseHeadersModifier(response)

    # For any other method of access, returning a new blank online prescription page
    else:

        # Editing response headers so as to ignore cached versions of pages
        response = render(request, "HealthCentre/prescriptionPortal.html")
        return responseHeadersModifier(response)

def responseHeadersModifier(response):
    """Funtion to edit response headers so that no cached versions can be viewed. Returns the modified response."""
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response

def requestSessionInitializedChecker(request):
    """Function to initialize request sessions if they don't exist."""

    # Try except for KeyError
    try:
        # Checking if session variables exist
        if request.session['goToAppointmentsPage'] and request.session['CreatenewAppointment'] and request.session['isDoctor'] and request.session['isLoggedIn'] and request.session['userEmail'] and request.session['Name'] and request.session['numberNewPrescriptions'] and request.session['writeNewPrescription']:
            # Do nothing if they do exist
            pass
    except:
        # Initialize request variables if they don't exist
        request.session['isDoctor'] = ""
        request.session['isLoggedIn'] = False
        request.session['userEmail'] = ""
        request.session['Name'] = ""
        request.session['numberNewPrescriptions'] = ""
        request.session['writeNewPrescription'] = False
        request.session['CreatenewAppointment'] = False
        request.session['goToAppointmentsPage'] = False
 
    # Returning request
    return request















    




































































































def whatsappNotification():
    # try:
    #     whatsapp_number = WhatsAppNumber.objects.get(id=number_id)
    #     return render(request, 'whatsapp_number.html', {'whatsapp_number': whatsapp_number})
    # except WhatsAppNumber.DoesNotExist:
    #     return render(request, 'error.html', {'message': 'WhatsApp number not found'})


    whatsappApi("+917904427507")

whatsappNotification()
    # return whatsappNotification()