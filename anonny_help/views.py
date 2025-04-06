from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import IncidentReportForm, AppointmentForm
from .models import IncidentReport, ChatSession, Article, HealthProgram
from django.contrib.auth.models import User

def index(request):
    # This could be a landing page with links to the main features of the platform
    return render(request, "anonny_help/index.html")
def login(request):
    # This is a placeholder for the login view
    # In a real application, you would use Django's built-in authentication views
    return render(request, "anonny_help/login.html")

def logout(request):
    # This is a placeholder for the logout view
    # In a real application, you would use Django's built-in authentication views
    return redirect("anonny_help/index")

def register(request):
    # This is a placeholder for the registration view
    # In a real application, you would use Django's built-in authentication views
    return render(request, "anonny_help/register.html")
# Anonymous incident reporting
def report_incident(request):
    if request.method == "POST":
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            # For anonymous reports, we do not assign a user
            incident.reported_by = None  
            incident.save()
            return JsonResponse({"status": "success", "report_id": incident.id})
        else:
            return JsonResponse({"status": "error", "message": "Invalid data provided"})
    else:
        form = IncidentReportForm()
    return render(request, "report_incident.html", {"form": form})

# Request help - could serve as an endpoint for students to ask for help (e.g., via a button)
def request_help(request):
    # For simplicity, we assume the request is a POST request coming from a mobile app
    if request.method == "POST":
        # Process the help request, e.g., log it and notify available healthcare workers
        return JsonResponse({"status": "success", "message": "Help is on the way"})
    return render(request, "request_help.html")

# Chat with a counselor
@login_required
def start_chat(request):
    # For demonstration, select a counselor (e.g., first staff user)
    counselor = User.objects.filter(is_staff=True).first()
    if counselor:
        session = ChatSession.objects.create(student=request.user, counselor=counselor)
        return JsonResponse({"status": "success", "chat_id": session.id})
    else:
        return JsonResponse({"status": "error", "message": "No counselor available"})

# Scheduling an appointment
@login_required
def schedule_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.student = request.user
            # For simplicity, assign a counselor (e.g., first available)
            appointment.counselor = User.objects.filter(is_staff=True).first()
            appointment.save()
            return JsonResponse({"status": "success", "appointment_id": appointment.id})
        else:
            return JsonResponse({"status": "error", "message": "Invalid appointment data"})
    else:
        form = AppointmentForm()
    return render(request, "appointment.html", {"form": form})

# Access informational content
def view_information(request):
    articles = Article.objects.all().order_by('-published_date')
    programs = HealthProgram.objects.all()
    context = {
        "articles": articles,
        "programs": programs,
    }
    return render(request, "info.html", context)
