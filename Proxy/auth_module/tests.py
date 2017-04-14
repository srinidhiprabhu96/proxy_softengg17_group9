from django.test import *
from auth_module.models import *
from django.contrib.auth.models import User

# Create your tests here.

# Test cases for auth module written by Hemanth
class AuthTestCase(TestCase):

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

	def test_signup(self) :
		response = self.client.get("/signup/")
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'signup.html')

	def test_login(self) :
		response = self.client.get("/login/")
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'login.html')

	def test_logout(self) :
		response = self.client.get("/logout/")
		self.assertRedirects(response,'/login/',status_code = 302,target_status_code = 200)
		
	def test_before_verify(self) :
		response = self.client.post("/verify/", {'name' : 'Prof' , 'email' : 'prof@iitm.ac.in'})
		self.assertTemplateUsed(response,'verify.html')
		response = self.client.post("/verify/", {'name' : 'Prof' , 'email' : 'prof@gmail.com'})
		self.assertRedirects(response,'/signup/',status_code = 302,target_status_code = 200)
		response = self.client.post("/verify/", {'name' : 'Stud' , 'email' : 'cs14b028@smail.iitm.ac.in'})
		self.assertTemplateUsed(response,'verify.html')	

	def test_auth(self) :
		response = self.client.post("/auth/", {'email' : 'testprof@iitm.ac.in' , 'password' : '123'})
		#print response
		self.assertRedirects(response,'/prof_home/',status_code = 302,target_status_code = 200)
		response = self.client.post("/auth/", {'email' : 'testprof@iitm.ac.in' , 'password' : '456'})
		self.assertRedirects(response,'/login/',status_code = 302,target_status_code = 200)
		response = self.client.post("/auth/", {'email' : 'teststud@smail.iitm.ac.in' , 'password' : '123'})
		#print response
		self.assertRedirects(response,'/stud_home/',status_code = 302,target_status_code = 200)
		response = self.client.post("/auth/", {'email' : 'teststud@smail.iitm.ac.in' , 'password' : '456'})
		self.assertRedirects(response,'/login/',status_code = 302,target_status_code = 200)

	def test_finish_signup(self) :
		response = self.client.post("/finish-signup/", {'name' : 'Stud','email' : 'cs14b028@smail.iitm.ac.in' , 'password' : '123' , 'confirm_password' : '123'})	
		self.assertTemplateUsed(response,'finish_signup.html')
		response = self.client.post("/finish-signup/", {'name' : 'Stud','email' : 'cs14b028@smail.iitm.ac.in' , 'password' : '123' , 'confirm_password' : '456'})
		self.assertTemplateUsed(response,'password_signup_page.html')
		response = self.client.get("/finish-signup/", {'name' : 'Stud','email' : 'cs14b028@smail.iitm.ac.in' , 'password' : '123' , 'confirm_password' : '123'})				
		self.assertRedirects(response,'/signup/',status_code = 302 , target_status_code = 200)

	def test_after_verify(self) :
		response = self.client.get("/verification/",{'code' : 'y789hj'})		
		self.assertTemplateUsed(response,'password_signup_page.html')
		response = self.client.post("/verification/",{'code' : 'y789hj'})		
		self.assertRedirects(response,'/signup/',status_code = 302 , target_status_code = 200)
