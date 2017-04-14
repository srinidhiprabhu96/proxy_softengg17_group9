from django.test import TestCase, Client
from auth_module.models import *
from prof_module.models import *
from stud_module.models import *
from django.contrib.auth.models import User
from django.http.request import HttpRequest
import datetime

# Create your tests here.
# Tests for prof module written by Pavan
class ProfTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.u1 = User.objects.create(username="testuser@smail.iitm.ac.in",first_name="Tester",is_staff='0')
		self.u1.set_password('123')
		self.u1.save()
		u2 = User.objects.create(username="testprof@iitm.ac.in",first_name="TesterProf",is_staff='1')
		u2.set_password('123')
		u2.save()
		c = Course.objects.create(course_id="CS1100",course_name="Computational Engineering",taught_by=u2,taken_by=[self.u1])
		c.save()
		att = Attendance.objects.create(course_id="CS1100", student=self.u1, prof=u2, date=datetime.date.today())
		att.save()
		q = Query.objects.create(course_id="CS1100", student=self.u1, date=datetime.date.today(), query='qwe qwe')
		q.save()

	def test_prof_home(self):
		# If prof logs in, he must be shown the prof's home page.
		self.client.login(username="testprof@iitm.ac.in",password="123")
		response = self.client.get('/prof_home/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'prof_home.html')

		# If student logs in and he tries to access prof's home page he must be redirected to login page
		self.client.login(username="testuser@smail.iitm.ac.in",password="123")
		response = self.client.get('/prof_home/')
		#print response
		self.assertRedirects(response,'/login/',status_code=302, target_status_code=200)

		# If a person is not logged in and tries to access prof home page, he must be redirected to login page
		response = self.client.get('/prof_home/')
		self.assertRedirects(response,'/login/',status_code=302, target_status_code=200)

	def test_prof_course(self):
		# If prof is logged in and requests a course he has taken.
		self.client.login(username="testprof@iitm.ac.in",password="123")
		response = self.client.get('/prof_course/CS1100/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'prof_course.html')

		# If prof is logged in and requests a course they don't teach.
		response = self.client.get('/prof_course/CS1101/')
		self.assertEqual(response.status_code,404)

	def test_prof_daily_report(self):
		# Prof enters a valid date and makes get request
		self.client.login(username="testprof@iitm.ac.in",password="123")
		response = self.client.get('/daily_report/CS1100/2017/04/09/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'daily_report.html')

		# Making an invalid get request because date part is wrong, raises http 404
		response = self.client.get('/daily_report/CS1100/17/4/10/')
		self.assertEqual(response.status_code,404)

		# Making an invalid get request because course part is wrong, raises http 404
		response = self.client.get('/daily_report/CS100/2017/4/10/')
		self.assertEqual(response.status_code,404)

	def test_prof_history(self):
		# Prof enters a valid date and makes get request
		self.client.login(username="testprof@iitm.ac.in",password="123")
		response = self.client.post('/prof_history/CS1100/',{'date':'03/04/2017'})
		self.assertRedirects(response,'/daily_report/CS1100/2017/04/03/',status_code=302, target_status_code=200)

		# Making an invalid get request because date part is wrong, raises http 404
		response = self.client.post('/prof_history/CS1100/',{'date':'3/4/17'})
		self.assertEqual(response.status_code,404)

	def test_prof_query(self):
		self.client.login(username="testprof@iitm.ac.in",password="123")
		q = Query.objects.get(course_id="CS1100", student=self.u1, date=datetime.date.today())
		self.client.post('/prof_queries/CS1100/',{'query':str(q.id)+' 1'})
		att = Attendance.objects.get(course_id="CS1100", student=self.u1, date=datetime.date.today())
		q = Query.objects.get(course_id="CS1100", student=self.u1, date=datetime.date.today())
		self.assertEqual(att.is_present,'1')
		self.assertEqual(q.status,'1')
