from django.test import TestCase, Client
from auth_module.models import *
from django.contrib.auth.models import User
from django.http.request import HttpRequest

# Create your tests here.
# To run these tests, "./manage.py test stud_module.tests" from Proxy.

class StudentTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		u = User.objects.create(username="testuser@smail.iitm.ac.in",first_name="Tester",is_staff='0')
		u.set_password('123')
		u.save()
		u = User.objects.create(username="testprof@smail.iitm.ac.in",first_name="TesterProf",is_staff='1')
		u.set_password('123')
		u.save()
	# Name each test case starting with "test_". Only asserts in these functions will be tested.
	def test_hello_function(self):
		self.assertIs(False,False)
	
	# Test if requesting login indeed gives the login page.	
	def test_request(self):
		response = self.client.get('/login/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'login.html')
	
	# A student logs in. Check if he is shown the stud_home page.	
	def test_login_of_student(self):
		self.client.login(username="testuser@smail.iitm.ac.in",password="123")
		response = self.client.get('/stud_home/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'stud_home.html')
	
	# Prof tries to access student home page	
	def test_prof_access_to_student_home(self):
		self.client.login(username="testprof@smail.iitm.ac.in",password="123")
		response = self.client.get('/stud_home/')
		self.assertRedirects(response,'/login/',status_code=302, target_status_code=200)
		
	def test_unknown_access_to_student_home(self):
		pass
