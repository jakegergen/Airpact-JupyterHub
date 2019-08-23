import subprocess
import crypt
from jupyterhub.auth import Authenticator
import jupyterhub.user
import requests
#####################MAIN IDEA########################################
#Jupyterhub used the unix ect/passwd file to verify login and password. 
#To add a user to the jupyter hub system they first must be added to the unix system
#when a request is made through the rest api to tell jupyter hub to look into
#the /etc/passwd files for loginid, path and (the /etc/shadow for the password) * ONLY SEARCHED FOR ON LOGIN, NOT REGISTRATION
#Username is stored in 
######################################################################


#1. ask user for name, and verify
#2. ask for password and verify
#3. run linux command to add user using unix protocol
#4. call the rest api /user/{name} to begin jupyter add user protocol described above


################TEST DRIVER######################
def userSetup():
	print("Login: ")
	login = input()
	#this is where I can make a rest api GET request using /users/{name}
	#and if no user then we may proceed, else name taken ask for a new name
	#but for now I will continue 
	print("Please enter your password")
	passwrd = input()
	return login, passwrd
################TEST DRIVER######################


################UNIX DRIVER######################
#Create a user to the unix machine
def unixAddUser(login,passwrd):
	encPass = crypt.crypt(passwrd,"42") #unix uses a seeded encription system, in this case '42' is the seed
	status = subprocess.run(["sudo", "adduser",login ]) #run command "sudo adduser <username>"
	print("Return code: ",status.returncode,"stdout: ", status.stdout) #print return value for debug
#################################################


################API REQUEST######################
#Add a registered unix user to the jupyterhub data base
#PARAM: the user name of the unix user. No password needed.
def juphubAddUser(login):
    base ="http://localhost:8000"
    route = "/hub/api/users/" + login
	URL = base + route #URL is a combination of the domain name, and the route 
	token = "b3a5fdb9b62645d79218d2d326c342f3" #token supplied by jupyterhub control panel. For security
	r = requests.post(url=URL,
		headers={ 'Authorization':'token %s' % token}) #send a post request url at described route witht the auth token
                                                       #to alert the jupyterhub process that a new user can be added to the system

##################################################

login, passwd = userSetup()
unixAddUser(login,passwd)
juphubAddUser(login)
print("done")
