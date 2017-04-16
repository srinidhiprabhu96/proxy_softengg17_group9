from django.test import *
from auth_module.models import *
from django.contrib.auth.models import User

# Create your tests here.
# Name each test case starting with "test_". Only asserts in these functions will be tested.
# To run these tests, "./manage.py test auth_module.tests" from Proxy.
# Test cases for auth module written by Hemanth
class AuthTestCase(TestCase):
	#Creating SignUp and User objects for testing
	def setUp(self) :
		self.client = Client()	
		u = SignUp.objects.create(name = "Stud" , email = "cs14b028@smail.iitm.ac.in" , code = "6jgfg8" , account = '0' , status = '1')
		u.save()
		u = SignUp.objects.create(name = "Prof" , email = "prof@iitm.ac.in" , code = "y789hj" , account = '1' , status = '1')
		u.save()
		u = User.objects.create(username = "teststud@smail.iitm.ac.in",first_name = "TestStud" , is_staff = '0')
		u.set_password('123')
		u.save()
		u = User.objects.create(username = "testprof@iitm.ac.in",first_name = "TestProf" , is_staff = '1')
		u.set_password('123')
		u.save()
		
	#Testing SignUp
	def test_signup(self) :
		response = self.client.get("/signup/")
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'signup.html')
		
	#Testing Login
	def test_login(self) :
		response = self.client.get("/login/")
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'login.html')
		
	#Testing logout
	def test_logout(self) :
		self.client.login(username="teststud@smail.iitm.ac.in",password="123")
		response = self.client.get("/logout/")
		self.assertRedirects(response,'/login/',status_code = 302,target_status_code = 200)
		
	#Testing the page before verification		
	def test_before_verify(self) :
	
		#Success upon Verification
		response = self.client.post("/verify/", {'name' : 'Prof' , 'email' : 'prof@iitm.ac.in'})
		self.assertTemplateUsed(response,'verify.html')
		
		#Invalid Email Ids redirects back to Signup Page
		response = self.client.post("/verify/", {'name' : 'Prof' , 'email' : 'prof@gmail.com'})
		self.assertRedirects(response,'/signup/',status_code = 302,target_status_code = 200)
		response = self.client.post("/verify/", {'name' : 'Stud' , 'email' : 'cs14b028@smail.iitm.ac.in'})
		self.assertTemplateUsed(response,'verify.html')
			
	#Testing Authentication Page
	def test_auth(self) :
		response = self.client.post("/auth/", {'email' : 'testprof@iitm.ac.in' , 'password' : '123'})
		self.assertRedirects(response,'/prof_home/',status_code = 302,target_status_code = 200)
		#Redirected to Professor Home on success
		
		response = self.client.post("/auth/", {'email' : 'testprof@iitm.ac.in' , 'password' : '456'})
		self.assertRedirects(response,'/login/',status_code = 302,target_status_code = 200)
		#Redirected back to login upon failure
		
		response = self.client.post("/auth/", {'email' : 'teststud@smail.iitm.ac.in' , 'password' : '123'})
		self.assertRedirects(response,'/stud_home/',status_code = 302,target_status_code = 200)
		#Redirected to Student Home on success
		
		response = self.client.post("/auth/", {'email' : 'teststud@smail.iitm.ac.in' , 'password' : '456'})
		self.assertRedirects(response,'/login/',status_code = 302,target_status_code = 200)
		#Redirected back to login upon failure
		
	#Testing after completing SignUp
	def test_finish_signup(self) :
	
		#Shown finish_signup upon success
		response = self.client.post("/finish-signup/", {'name' : 'Stud','email' : 'cs14b028@smail.iitm.ac.in' , 'password' : '123' , 'confirm_password' : '123'})	
		self.assertTemplateUsed(response,'finish_signup.html')
		response = self.client.post("/finish-signup/", {'name' : 'Stud','email' : 'cs14b028@smail.iitm.ac.in' , 'password' : '123' , 'confirm_password' : '456'})
		self.assertTemplateUsed(response,'password_signup_page.html')
		
		#Redirected to signup upon success
		response = self.client.get("/finish-signup/", {'name' : 'Stud','email' : 'cs14b028@smail.iitm.ac.in' , 'password' : '123' , 'confirm_password' : '123'})				
		self.assertRedirects(response,'/signup/',status_code = 302 , target_status_code = 200)
		
	#Testing page after verification
	def test_after_verify(self) :
	
		#Shown password signup upon success
		response = self.client.get("/verification/",{'code' : 'y789hj'})		
		self.assertTemplateUsed(response,'password_signup_page.html')
		
		#Redirected to signup upon success
		response = self.client.post("/verification/",{'code' : 'y789hj'})		
		self.assertRedirects(response,'/signup/',status_code = 302 , target_status_code = 200)
