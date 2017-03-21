This is for the Proxy project 

Done by
Srinidhi
Pavan
Vinod
Satish
Hemanth

Please do not change the directory structure. We need to add files in appropriate locations as we proceed.  

First install Django.  

To run the server,  
cd Proxy  
python manage.py runserver  

Then on your browser type the address(for example 127.0.0.1:8080) and see the basic web page.  

To make sure that changes in models take place, do:  
	1) python manage.py check  
	2) python manage.py makemigrations <app_name>  
	3) python manage.py migrate  
	In case of any errors, resolve them.  
	
To access the DB from command line:  
	1) python manage.py shell - This will open a python command prompt. In that you can import the models you want and change the DB.  
	
To IMPROVE in auth_module:
	1) Delete the entry from SignUp DB in 24 hours( or come up with a hack that stores the time stamp and adds to DB only if the timestamps are >24 hours)   
	2) Currently, there doesn't seem to be any way to check if the e-mail ID is valid(For ex: cs14b068@smail.iitm.ac.in is not valid, but our module will send the mail and display "Verification mail sent"). This is a possible source of crashing the DB. Since we only do a regex check, a malicious program could signup many times with different random addresses that match the regex. If possible, this thing should be looked into. (Even if such a module exists, it would take some time for the verification to happen. It is upto our design whether we want to spend this extra time for every signup or "assume" that no such harmful attack will happen.)  
	
AUTH module features implemented(fully done):
	1) If email already present in DB, doesn't create a new row, just says mail resent and resends the mail.  
	2) Reg-Ex matching and giving account type(prof or student)  
	3) In case email doesnt match regex, or some failure in connection etc. occurs, takes back to signup page and displays the message.  
	4) Click on link in e-mail, if the code exists, enter the password and signup process will be finished.  
	5) Password is stored as hash.  
	6) If the verification link is clicked again after succesful signup, it will say that the URL has already been modified.  
	7) If a person attempts to signup for an email which already exists as a user, the appropraite message is displayed.  
	

