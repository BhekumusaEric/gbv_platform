from django import forms
from .models import IncidentReport, Appointment

class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ['incident_type', 'description', 'location']
        # We do not require a reported_by field as reports can be anonymous

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'notes']
