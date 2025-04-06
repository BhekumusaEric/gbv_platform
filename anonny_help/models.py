from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Incident report from a student (anonymous)
class IncidentReport(models.Model):
    INCIDENT_TYPE_CHOICES = [
        ('GBV', 'Gender-Based Violence'),
        ('Cyberbullying', 'Cyberbullying'),
    ]
    # Note: Since students report anonymously, we store a flag rather than the user
    reported_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, help_text="May be null for anonymous reports")
    incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    date_reported = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.incident_type} reported on {self.date_reported:%Y-%m-%d}"

# Appointment for counseling sessions
class Appointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    counselor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="counselor_appointments")
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Appointment: {self.student.username} with {self.counselor.username} on {self.appointment_date:%Y-%m-%d %H:%M}"

# Chat session between a student and a healthcare worker/counselor
class ChatSession(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_sessions")
    counselor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_counselor_sessions")
    started_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"ChatSession: {self.student.username} & {self.counselor.username}"

# Chat message in a chat session
class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp:%H:%M}"

# Informational articles and health program content
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class HealthProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name
