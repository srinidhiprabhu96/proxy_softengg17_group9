This project is done as a part of CS3410 in the Jan - May 2017 semester at IIT Madras.

This project is done by Group 9. The group members are -

* Srinidhi Prabhu, CS14B028, srinidhiprabhu96@gmail.com, +919480258046, +919790463346
* Sai Pavan D, CS14B041, saipvn4@gmail.com, +91 9790464704
* Vinod
* Satish
* Hemanth

This project needs django to run. To install, please run :
	`sudo pip2 install -r requirements.txt`

To run the server:  
	`cd Proxy`  
	`python manage.py runserver`

If running the server for the first time, you may have to run migrations:        
	`python manage.py makemigrations auth_module stud_module prof_module`         
	`python manage.py migrate`

Then on your browser type the address(for example 127.0.0.1:8080) to go to the login page.  

We use the default Django "User" model (in django.contrib.auth.models) to store the users. This makes logging in and logging out, checking if the person trying to access the page is logged in etc. easier. We use the is_staff attribute to check if the user is a professor or a student.

To make sure that changes in models(models are similar to tables for the DB) take place, do:  
	`python manage.py check`     
	`python manage.py makemigrations <module_name>`        
	`python manage.py migrate`    
	In case of any errors, resolve them.  

To access the DB from command line:  
	`python manage.py shell`   
	This will open a python command prompt. In that, you can import the models you want and change the DB.  

AUTH MODULE  	  
	Things that can be improved in future in auth_module:   
		1) Delete the entry from SignUp DB in 24 hours( or come up with a hack that stores the time stamp and adds to DB only if the timestamps are > 24 hours)   
		2) Currently, there doesn't seem to be any way to check if the e-mail ID is valid(For ex: cs14b068@smail.iitm.ac.in is not valid, but our module will send the mail and display "Verification mail sent"). This is a possible source of crashing the DB. Since we only do a regex check, a malicious program could signup many times with different random addresses that match the regex. If possible, this thing should be looked into. We tried out a few tools, but they did not work.  

  AUTH module features implemented(fully done)  
	        1) If email already present in DB, doesn't create a new row, just says mail resent and resends the mail.  
		2) Reg-Ex matching and giving account type(prof or student)  
		3) In case email doesnt match regex, or some failure in connection etc. occurs, takes back to signup page and displays the message.  
		4) Click on link in e-mail, if the code exists, enter the password and signup process will be finished.  
		5) Password is stored as hash.  
		6) If the verification link is clicked again after succesful signup, it will say that the URL has already been modified.  
		7) If a person attempts to signup for an email which already exists as a user, the appropriate message is displayed.  

ADMIN SIDE   
	The functions for the admin are included in the "admin_functions" folder in the "functions.py" file. Further instructions to run this script and other details are provided in the file.

Common static includes all the static files such as JS and CSS files used across the various HTML pages.

dummy_entries.py  
	This file includes code to add some database entries. To run the script:       
	`python manage.py shell`       
	In the shell, run:     
	`execfile("dummy_entries.py")`      
	If there are errors, manually copy-paste the lines of the code from the file into the shell to add the database entries.

All photos uploaded by a professor are included in the "media" folder.

sendEmail.py   
	This file includes code to send an email. This is called as a separate process during the signup process. More details(regarding implementation) can be found in the file.

searchFace.py  
	This file includes code to detect faces in an image and search for the detected faces in a course. This is also called as a separate process when a professor uploads photos to take attendance. More details can be found in the file.

STUD MODULE   
	Includes functions called when a student is logged in.

PROF MODULE  
	Includes functions called when a professor is logged in.

Issues have been created on github to keep track of what things were to be done. Feel free to raise more issues, if needed
