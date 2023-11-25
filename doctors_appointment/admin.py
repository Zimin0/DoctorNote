from django.contrib import admin
from doctors_appointment.models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'address', 'office_number', 'health_troubles')
    list_filter = ('patient', 'doctor', 'date', 'time')
    search_fields = ('patient', 'doctor', 'date', 'time')

admin.site.register(Appointment, AppointmentAdmin)
