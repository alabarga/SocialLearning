#!/usr/bin/python
import urllib, urllib2, json, re
import xml.etree.ElementTree as et

def apiRequestDelicious(auth, call, args = None):
	headers = { }
	url = ''
	if call == 'oauth/token':
		args = {'client_id' : auth['delicious_clientid'],
				'client_secret' : auth['delicious_clientsecret'],
				'grant_type' : 'credentials',
				'username' : auth['username'],
				'password' : auth['password']
		}
		url = "https://avosapi.delicious.com/api/v1/oauth/token"

	else:
		url = "https://avosapi.delicious.com/api/v1/" + call
		headers = { 'Authorization' : "Bearer " + str(auth) }

	# Prepare request.
	data = None
	if args != None:
		data = urllib.urlencode(args)

	#req = urllib2.Request(url, data, headers)
	req = urllib2.Request(url, data, headers)

	# Execute request.
	response = urllib2.urlopen(req)
	result = response.read()
	return result

def getDeliciousToken(username, password, delicious_clientid, delicious_clientsecret):
	try:
		auth = {
			'username' : username,
			'password' : password,
			'delicious_clientid' : delicious_clientid,
			'delicious_clientsecret' : delicious_clientsecret 
		}
		tmp = apiRequestDelicious(auth, 'oauth/token')
		json_data = json.loads(tmp)
		return json_data['access_token']
	except Exception, e:
		return False

def getDeliciousTags(token):
	try:
		tmp = apiRequestDelicious(token, "tags/get")
		tree = et.fromstring(tmp)

		tags = []
		# Convert into DICT array. 
		for i in range(len(tree)):
			tag = { 'tag' : tree[i].attrib['tag'],
				'count' : tree[i].attrib['count']
			}
			tags.append(tag)
		return tags
	except Exception, e:
		return False

def getDeliciousPosts(token):
	try:
		tmp = apiRequestDelicious(token, "posts/all")
		tree = et.fromstring(tmp)

		posts = []
		# Convert into DICT array.
		for i in range(len(tree)):
			post = { 'description' : tree[i].attrib['description'],
				'extended' : tree[i].attrib['extended'],
				'hash' : tree[i].attrib['hash'],
				'href' : tree[i].attrib['href'],
				'private' : tree[i].attrib['private'],
				'shared' : tree[i].attrib['shared'],
				'tag' : tree[i].attrib['tag'],
				'time' : tree[i].attrib['time']
			}
			posts.append(post)
		return posts
	except Exception, e:
		return False

def countDeliciousMediaWithTag(posts, tagname):
	count = 0
	for post in posts:
		if re.match(".* " + tagname + " .*", post['tag'], re.M|re.I) or re.match("^" + tagname + " .*", post['tag'], re.M|re.I) or re.match(".* " + tagname + "$", post['tag'], re.M|re.I):
			count += 1
	return count

def checkDeliciousMediaTag(post, tagname):
	if re.match(".* " + tagname + " .*", post['tag'], re.M|re.I) or re.match("^" + tagname + " .*", post['tag'], re.M|re.I) or re.match(".* " + tagname + "$", post['tag'], re.M|re.I):
		return True
	else:
		return False
