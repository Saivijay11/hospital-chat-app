# Import Django test utilities and DRF test client
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import CustomUser, ApprovedDoctor
from rest_framework import status

# Test class for registration and login functionality
class UserAuthTests(TestCase):

    # This method runs before each test to initialize reusable objects
    def setUp(self):
        self.client = APIClient()  # API client for simulating requests

        # added an approved doctor entry to check the preverified doctors
        self.approved_doctor = ApprovedDoctor.objects.create(
            doctor_id="DOC123", full_name="Dr. Vijay"
        )

        # end points are defined by using urls.py
        self.register_url = reverse('register')      #registration endpoint and the one below us for login using token endpoint
        self.login_url = reverse('token_obtain_pair') 

    #testing for a patient for regsitration process completion
    def test_patient_registration(self):
        data = {
            "username": "ravi",
            "email": "ravisaiappa@gmail.com",
            "password": "Ravi@12345",
            "full_name": "Ravi Kumar",
            "address": "17711 Misty grove",
            "blood_type": "A+",
            "role": "patient"  # this helps to determine patient or doctor
        }
        response = self.client.post(self.register_url, data, format='json')

        # rturn successful patient registration with 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # making sure that user is now stored in the database
        self.assertTrue(CustomUser.objects.filter(username="ravi").exists())

    # testign a doctor with all the required fields crrtly so he can register
    def test_doctor_registration_with_valid_id(self):
        data = {
            "username": "Prasad",
            "email": "saivijayp2@gmail.com",
            "password": "Sai@12345",
            "full_name": "Prasad Kumar",
            "address": "4932 walking tk",
            "blood_type": "B+",
            "role": "doctor",
            "doctor_id": "DOC123"  # doc id is check for validation
        }
        response = self.client.post(self.register_url, data, format='json')

        #will return that registration is successful at 201 code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #make sure the user who has been created has the bool flag doctor to true
        self.assertTrue(CustomUser.objects.get(username="Prasad").is_doctor)

    # checking with invalid doctor id
    def test_doctor_registration_with_invalid_id(self):
        data = {
            "username": "sathvik",
            "email": "sathvik1@gmail.com",
            "password": "Sathvik@123",
            "role": "doctor",
            "doctor_id": "INVALID"  # invalid is passed to check
        }
        response = self.client.post(self.register_url, data, format='json')

        # Should return 400 Bad Request due to invalid doctor_id
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # testing by login with username in place of email
    def test_login_with_username(self):
        # Create the user first
        user = CustomUser.objects.create_user(
            username="ravi",
            email="ravisaiappa@gmail.com",
            password="Ravi@12345",
            is_patient=True
        )

        # trying to login using usrname
        data = {
            "username": "ravi",
            "password": "Ravi@12345"
        }
        response = self.client.post(self.login_url, data, format='json')

        # returns login successful with 200 ok
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    # email instead of username
    def test_login_with_email(self):
        #user with mail and username created
        user = CustomUser.objects.create_user(
            username="ravi",
            email="ravisaiappa@gmail.com",
            password="Ravi@12345",
            is_patient=True
        )

        # login using mail
        data = {
            "username": "ravisaiappa@gmail.com",  # use mail in placed of username
            "password": "EmailPass123!"
        }
        response = self.client.post(self.login_url, data, format='json')

        #return successfuly domne along with token
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
