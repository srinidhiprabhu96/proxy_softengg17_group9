# -*- coding: utf-8 -*-
import urllib2
import urllib
import time

api_key = "f4EgW60XiioU-gWYEmNqy9Vsvdq_gMap"	# API Key to use Face++ services
api_secret = "_QBW4ClvR0wjugjLInRvOd7KN4obJd1l"	# API secret to use Face++ services

""" List of URLs for the API calls	"""
faceset_create_url = "https://api-us.faceplusplus.com/facepp/v3/faceset/create"
faceset_add_url = "https://api-us.faceplusplus.com/facepp/v3/faceset/addface"
detect_url = "https://api-us.faceplusplus.com/facepp/v3/detect"
search_url = "https://api-us.faceplusplus.com/facepp/v3/search"

""" End of URLs for API calls 	"""

"""
Usage
#createFaceSet("CS3410")
#detectFace("../images/images/CS14B0XX.jpg")
#addFaceSet("CS3410", ["a7b1d6c7baa05ef7043e0d11cd32da12", "e34875caf029ebb55b2d1351c25453e3", "2019b7bba5e794ac94073aac96adebed", "cf4c11367a775f3f9c5fb9515f190e2c"])
#searchFace("CS3410",image_path="../images/images2/CS14B0YY.jpg") or searchFace("CS3410",face_token="2019b7bba5e794ac94073aac96adebed")
"""

# This function is to be called when a new course is created by the admin. The faceset will later contain the face tokens of all the students in the course.
def createFaceSet(course_number):
	global api_key
	global api_secret
	global faceset_create_url
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
	data.append(api_key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
	data.append(api_secret)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'outer_id')
	data.append(course_number)
	data.append('--%s--\r\n' % boundary)
	
	make_request(faceset_create_url,data,boundary)


# This function is to be called during upload training data, after getting the face tokens. We can add atmost 5 face tokens to a faceset at a time. The input argument 'face_tokens' should be a list.
# Cupping for some reason, try with postman
def addFaceSet(course_number,face_tokens):
	global api_key
	global api_secret
	global faceset_add_url
	if len(face_tokens) > 5:
		raise Exception("At most 5 faces can be added at a time")
	face_token_string = ",".join(face_tokens)
	#print face_token_string
	
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
	data.append(api_key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
	data.append(api_secret)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'outer_id')
	data.append(course_number)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'face_tokens')
	data.append(face_token_string)
	data.append('--%s--\r\n' % boundary)
	
	make_request(faceset_add_url,data,boundary)
	
# This function is to be called during take attendance. We can pass either of "image_path" or "face_token". We get the facetoken in the faceSet that matches this face. So, we need to store roll number - face token mapping.
def searchFace(course_number,image_path=None,face_token=None):
	global api_key
	global api_secret
	global search_url
	
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
	data.append(api_key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
	data.append(api_secret)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'outer_id')
	data.append(course_number)
	data.append('--%s' % boundary)
	if image_path:
		data.append('Content-Disposition: form-data; name="%s"; filename="image.jpg"' % 'image_file')
		data.append('Content-Type: %s\r\n' % 'application/octet-stream')
		fp = open(image_path,'rb')
		if fp:
			data.append(fp.read())
			fp.close()
		else:
			raise Exception("Image not found")
	elif face_token:		
		data.append('Content-Disposition: form-data; name="%s"\r\n' % 'face_token')
		data.append(face_token)
	else:
		raise Exception("Enter a face_token or image_path")
	data.append('--%s--\r\n' % boundary)
	
	make_request(search_url,data,boundary)

# This function is to be called to get a face token, prior to any operation that needs a face token(such as add face to faceset.	
def detectFace(image_path):
	global api_key
	global api_secret
	global detect_url
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
	data.append(api_key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
	data.append(api_secret)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"; filename="image.jpg"' % 'image_file')
	data.append('Content-Type: %s\r\n' % 'application/octet-stream')
	fp = open(image_path,'rb')
	if fp:
		data.append(fp.read())
		fp.close()
	else:
		raise Exception("Image not found")
	data.append('--%s--\r\n' % boundary)
	
	make_request(detect_url,data,boundary)
	
		
# Response part is currently here, we need to return values appropriately.		
def make_request(url,data,boundary):
	# From this part onward it is the same.
	http_body='\r\n'.join(data)
	#print http_body
	print "Building request"
	#buld http request
	req=urllib2.Request(url)
	#header
	req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
	req.add_data(http_body)
	try:
		#post data to server
		resp = urllib2.urlopen(req, timeout=5)
		#get response
		qrcont=resp.read()
		print qrcont

	except Exception,e:
		print 'http error',e
