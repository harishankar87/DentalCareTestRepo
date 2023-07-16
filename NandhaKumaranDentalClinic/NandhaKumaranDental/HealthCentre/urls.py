from django.urls import path

from . import views
# from django.urls import path
# from .views import get_whatsapp_number

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
    # path('whatsapp-number/<int:number_id>/', views.get_whatsapp_number, name='whatsapp_number'),
]

# from django.urls import path
# from your_app.views import get_whatsapp_number

# urlpatterns = [
#     # Other URL patterns...
#     path('whatsapp-number/<int:number_id>/', get_whatsapp_number, name='whatsapp_number'),
# ]
