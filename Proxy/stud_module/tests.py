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
		u = User.objects.create(username="testprof@iitm.ac.in",first_name="TesterProf",is_staff='1')
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
	
	"""
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
	
	# A person who is not logged in tries to access the student home page
	def test_unknown_access_to_student_home(self):
		response = self.client.get('/stud_home/')
		self.assertRedirects(response,'/login/',status_code=302, target_status_code=200)
	"""	
	def test_stud_home(self):
		# If student logs in, he must be shown the student's home page.
		self.client.login(username="testuser@smail.iitm.ac.in",password="123")
		response = self.client.get('/stud_home/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'stud_home.html')
		
		# If prof logs in and he tries to access student home page he must be redirected to login page
		self.client.login(username="testprof@iitm.ac.in",password="123")
		response = self.client.get('/stud_home/')
		#print response
		self.assertRedirects(response,'/login/',status_code=302, target_status_code=200)
		
		# If a person is not logged in and tries to access student home page, he must be redirected to login page
		response = self.client.get('/stud_home/')
		self.assertRedirects(response,'/login/',status_code=302, target_status_code=200)
				
	def test_stud_daily_report(self):
		# Student enters a valid date and makes post request
		self.client.login(username="testuser@smail.iitm.ac.in",password="123")
		response = self.client.post('/stud_daily_report/',{'date':'10/4/2017'})
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'stud_daily_report.html')
		
		# Making get request
		response = self.client.get('/stud_daily_report/',{'date':'10/4/2017'})
		self.assertRedirects(response,'/login/',status_code=302, target_status_code=200)
		
		# Making an invalid post request, raises http 404
		response = self.client.post('/stud_daily_report/')
		self.assertEqual(response.status_code,404)
