from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from anonny_help.models import IncidentReport, ChatSession, Article, HealthProgram, Appointment

class PlatformTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a counselor/healthcare worker (staff user)
        self.counselor = User.objects.create_user(
            username="counselor",
            email="counselor@example.com",
            password="password"
        )
        self.counselor.is_staff = True
        self.counselor.save()

        # Create a student user
        self.student = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="password"
        )
        
        # Create an article and health program so that the info page has content.
        Article.objects.create(title="Article 1", content="Content for article 1")
        HealthProgram.objects.create(name="Counseling Program", description="Counseling services", contact_info="1234567890")

    def test_report_incident_success(self):
        url = reverse('report_incident')
        data = {
            "incident_type": "GBV",
            "description": "Test incident description",
            "location": "Test location"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(json_resp.get("status"), "success")
        self.assertIsNotNone(json_resp.get("report_id"))
        # Optionally, check that the incident was created in the DB.
        self.assertEqual(IncidentReport.objects.count(), 1)

    def test_request_help(self):
        url = reverse('request_help')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(json_resp.get("status"), "success")
        self.assertEqual(json_resp.get("message"), "Help is on the way")
    
    def test_start_chat_requires_login(self):
        url = reverse('start_chat')
        # Without login, the view should redirect to the login page.
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Now, log in as a student and try again.
        self.client.login(username="student", password="password")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(json_resp.get("status"), "success")
        self.assertIsNotNone(json_resp.get("chat_id"))
        # Optionally, check that a ChatSession was created.
        self.assertEqual(ChatSession.objects.count(), 1)
    
    def test_schedule_appointment(self):
        url = reverse('schedule_appointment')
        # Without login, should redirect.
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        # Log in as student.
        self.client.login(username="student", password="password")
        data = {
            "appointment_date": "2030-01-01 10:00",
            "notes": "Need counseling help"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(json_resp.get("status"), "success")
        self.assertIsNotNone(json_resp.get("appointment_id"))
        # Optionally, ensure an Appointment object was created.
        self.assertEqual(Appointment.objects.count(), 1)
    
    def test_view_information(self):
        url = reverse('view_information')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check that the context contains articles and programs.
        self.assertIn("articles", response.context)
        self.assertIn("programs", response.context)
        self.assertGreater(len(response.context["articles"]), 0)
        self.assertGreater(len(response.context["programs"]), 0)

    # Example: Test unauthorized access to a protected resource.
    def test_access_private_data_unauthorized(self):
        # For endpoints that require a valid access token or login, you might simulate this:
        protected_url = reverse('start_chat')
        response = self.client.get(protected_url)
        self.assertEqual(response.status_code, 302)  # Expecting redirection to login

    # Additional tests can be added for:
    # - Incident deletion (if implemented)
    # - Blocking a user (if implemented)
    # - Encryption utilities (if implemented, e.g., via a utils function)
    
if __name__ == '__main__':
    TestCase.main()
