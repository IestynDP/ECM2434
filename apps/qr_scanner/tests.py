from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.accounts.models import Restaurant, UserCheckIn, account
from datetime import date
import json

class QRScannerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Creates a test user and logs them in
        self.account, created = account.objects.get_or_create(user=self.user, defaults={'points': 0, 'total_points': 0})
        # Ensures the user has an associated account with default points
        self.owner = User.objects.create_user(username='owner', password='ownerpassword')
        # Creates a test owner user
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', qrCodeID='12345', points=10, owner=self.owner)
        # Sets up a test restaurant with a QR code and points
        self.client.login(username='testuser', password='testpassword')
        # Logs in the test user

    def test_qr_scan_view(self):
        response = self.client.get(reverse('qr_scan'))
        self.assertEqual(response.status_code, 200)
        # Checks that the QR scan view is accessible
        self.assertTemplateUsed(response, 'qr_scan/qr_scan.html')
        # Verifies that the correct template is used for the QR scan view

    def test_scan_qr_view(self):
        response = self.client.get(reverse('scan_qr'))
        self.assertEqual(response.status_code, 200)
        # Checks that the scan QR view is accessible
        self.assertTemplateUsed(response, 'qr_scan/qr_scan.html')
        # Verifies that the correct template is used for the scan QR view

    def test_checkin_qrcode_valid_qr_code(self):
        data = {'qr_code_id': '12345'}
        response = self.client.post(reverse('checkin_qrcode'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Checks that the check-in QR code view is accessible with valid QR code
        self.assertJSONEqual(response.content, {
            'success': True,
            'already_scanned': False,
            'restaurant_name': 'Test Restaurant',
            'points': 10,
            'total_points': 10,
            'badges': []
        })
        # Verifies the JSON response contains the correct data for a valid QR code
        self.account.refresh_from_db()
        self.assertEqual(self.account.points, 10)
        self.assertEqual(self.account.total_points, 10)
        # Verifies that the user's points and total points are updated correctly

    def test_checkin_qrcode_invalid_qr_code(self):
        data = {'qr_code_id': 'invalid'}
        response = self.client.post(reverse('checkin_qrcode'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # Checks that the check-in QR code view returns a 400 status code for an invalid QR code
        self.assertJSONEqual(response.content, {'success': False, 'message': 'Invalid QR Code'})
        # Verifies the JSON response contains the correct error message for an invalid QR code

    def test_checkin_qrcode_missing_qr_code(self):
        data = {}
        response = self.client.post(reverse('checkin_qrcode'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # Checks that the check-in QR code view returns a 400 status code for a missing QR code
        self.assertJSONEqual(response.content, {'success': False, 'message': 'QR Code ID is missing'})
        # Verifies the JSON response contains the correct error message for a missing QR code

    def test_checkin_qrcode_already_scanned(self):
        UserCheckIn.objects.create(account=self.account, restaurant=self.restaurant, check_in_date=date.today())
        # Creates a check-in record for the user at the restaurant for today
        data = {'qr_code_id': '12345'}
        response = self.client.post(reverse('checkin_qrcode'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Checks that the check-in QR code view is accessible with a valid QR code that has already been scanned today
        self.assertJSONEqual(response.content, {
            'success': True,
            'already_scanned': True,
            'message': 'You already scanned today'
        })
        # Verifies the JSON response contains the correct message for an already scanned QR code

