from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name = "index"),
    path('register', views.register, name = "register"),
    path('doctors', views.doctors, name = "doctors"),
    path('login', views.login, name = "login"),
    path('emergency', views.emergency, name = "emergency"),
    path('logout', views.logout, name = "logout"),
    path('contactus', views.contactus, name = "contactus"),
    path('onlineprescription', views.onlineprescription, name = "onlineprescription"),
    path('doctorprofile', views.doctorprofile, name = "doctorprofile"),
    path('doctorappointments', views.doctorappointments, name = "doctorappointments"),
    path('doctorappointmentsfalse', views.doctorappointmentsfalse, name = "doctorappointmentsfalse"),
    path('editAppointments/<pk>', views.editAppointments, name = 'editAppointments'),
    path('deleteappointment/<pk>', views.deleteappointment, name = 'deleteappointment')
    # path('editAppointments', views.editAppointments, name = 'editAppointments')
]
