# openlog



import base64
import urllib.request
import json

sscount=0
ssin=False
ssend =False
sessions = []
ips=[]
sips=set()

PATH="f:/pyton/"
IN="smtp19.txt"
OUT="smtplog19.csv"
IP="ip.ip"

# открываем лог файл
log = open(PATH+IN,'r', encoding="windows-1251", errors='ignore')
# открываем файл с информацией по ip
ipf=open(PATH+IP,'r', encoding="UTF-8")
# считываем информацию по ip
for item in ipf:
	ip=item.split('|',2);
	if len(ip)<3: print ('error')
	ips.append(ip);
	if not(ip[0] in sips):
		sips.add(ip[0]);
ipf.close


def SSIpInfo(s):
	ans='none|none error*'+s+'*'
	if s in sips:
		for item in ips:
			#print(item)
			if item[0]==s:
				ans = item[1]+'|'+item[2].rstrip()
	else:
		sips.add(s)
		noerror= True
		country='none'
		city='none'
		try:
			getinfo = urllib.request.urlopen("https://ipinfo.io/"+ip+"?token=e9991633f8f11e")
			#getinfo = urllib.request.urlopen("http://www.geoplugin.net/json.gp?ip="+ip)#
			
		except:
			noerror = False
		if 	noerror:
			#print('OK')
			ginfo=json.load(getinfo)
			#print(ginfo)
			try:
				country=ginfo["country"]
			except:
				country="none"
			try:
				city=ginfo["city"]
			except:
				city="none"		
		ipf=open(PATH+IP,'a',encoding="UTF-8")
		ipf.write(str(s)+'|'+str(country)+'|'+str(city)+'\n');
		ipf.close
		ans= str(country)+'|'+str(city)
	return ans

def SSNumber(s):
	a=s.find('Session')+8
	b=s.find(';')
	return s[a:b]
	
def SSIp(s):
	a=s.find('connection from')+17
	b=a+s[a:].find(':')
	return s[a:b]
	
def SSAuthStatus(s):
	a=s.find('Authentication')+15;
	return s[a:]
	
def SSLogin(s):
	a=s.find('<--')+4
	try:
		s=base64.b64decode(s[a:])
	except:
		print (error, s);
		s = 'error'
	return s
	
def SSTo(s):
	a=s.find('RCPT TO:')+9
	return s[a:]

def SSFrom(s):
	a=s.find('MAIL FROM:')+11
	b=s.find('>')
	return s[a:b]
	
def SSLoginin(s):
	a=s.find('Authenticated as')+17
	return s[a:]
	
def SSAuth(s):
	if s.find('LOGIN')>0:
		return 'LOGIN'
	elif s.find('CRAM')>0:
		return 'CRAM-MD5'
	else:
		return ''
	
def SSLoginCram(s):
	a=s.find('<--')+4
	try:
		s=base64.b64decode(s[a:])
	except:
		print (error, s);
		s='*error* '
	a=str(s).find(' ')
	return s[:a]
	
def SSLoginPop(s):
	a=s.find('APOP ')+5
	b=s.rfind(' ')
	return s[a:b]
	
def SSLoginAuth(s):
	a=s.find('LOGIN')+6
	try:
		s1=base64.b64decode(s[a:])
	except:
		print ('error', s);
		s1='*error*'
	return s1
	
csv=open(PATH+OUT,'w',encoding="UTF-8")
session={'SSNumber':'','Proto':'','SSStart':'','SSStop':'','SSIp':'','AuthStatus':'','Login':'','TO':'','FROM':'','LoginIn':'','AUTH':'','Country':'','City':''}
for item in session:
	csv.write(item+'|')
csv.write('\n')


for line in log:
	# Находим начало сесии
	if line.find('Session ')>0:
		#print('test')
		ssin = True
		sslist = []
	if ssin:
		sslist.append(line)
		# находи конец сессии
		if line.find('---------')>0:
			ssend = True	
			ssin = False
	if ssend: # Анализируем сессию
			sscount=sscount+1
			
			session={
			'SSNumber':'',
			'Proto':'',
			'SSStart':'',
			'SSStop':'',
			'SSIp':'',
			'AuthStatus':'',
			'Login':'',
			'TO':'',
			'FROM':'',
			'LoginIn':'',
			'AUTH':'',
			'Country':'',
			'City':''
				}
			# Определяем номер сессии
			session["SSNumber"]=SSNumber(sslist[0].rstrip())
			# Определяем время старта сессии
			session["SSStart"]=sslist[0][4:23]
			# Определяем время конца сессии
			session["SSStop"]=sslist[-1][4:23]
			
			#print(session["SSNumber"])
			for item in sslist:
				if item.find('connection from')>0:
					ip=SSIp(item.rstrip())
					session["SSIp"]=ip
					if item.find('SMTP') > 0:
						session['Proto']='SMTP'
					if item.find('POP3') > 0:
						session['Proto']='POP3'
					if item.find('IMAP') > 0:
						session['Proto']='IMAP'
					info=str(SSIpInfo(ip))
					session["Country"]=info[:info.find('|')-1]
					session["City"]=info[info.find('|')+1:]
				#	noerror= True
				#	info = {}
				#		getinfo = urllib.request.urlopen("https://ipinfo.io/"+ip+"?token=e9991633f8f11e")
				#	except:
				#		noerror = False
				#	if 	noerror:
				#	if noerror != True:
				#		print ('Error',ip)
				#	if len(info)>0:
				#		try:
				#			session["Country"]=info["country"]
				#		except:
				#			session["Country"]="none"
						#try:
						#	session["City"]=info["city"]
						#except:
						#	session["City"]="none"
				if item.find('Authentication')>0:
					session["AuthStatus"]=SSAuthStatus(item.rstrip())
				if item.find ('334 VXN')>0:
					if sslist[sslist.index(item)+1].find('<--')>0:
						session["Login"]=str(session["Login"])+str(SSLogin(sslist[sslist.index(item)+1].rstrip()))+' '
				if item.find('RCPT TO')>0:
					session["TO"]=session['TO']+SSTo(item.rstrip())+' '
				if item.find('MAIL FROM')>0:
					session["FROM"]=SSFrom(item.rstrip())
				if item.find('Authenticated as')>0:
					session["LoginIn"]=SSLoginin(item.rstrip())
				if item.find('<-- AUTH')>0:
					session['AUTH']=str(session["AUTH"])+' '+SSAuth(item.rstrip())
				if item.find('<-- AUTH CRAM-MD5')>0:
					if sslist[sslist.index(item)+2].find('<--')>0:
						session["Login"]=str(session["Login"])+str(SSLoginCram(sslist[sslist.index(item)+2].rstrip()))+' '
				if item.find('<-- AUTH LOGIN')>0:
					if item.find('<-- AUTH LOGIN')+16<len(item):
						session["Login"]=str(session["Login"])+str(SSLoginAuth(item.rstrip()))+' '
				if item.find('<-- APOP')>0:
						session["Login"]=str(session["Login"])+str(SSLoginPop(item.rstrip()))+' '
							
			#sessions.append(session)
			for item in session:
				csv.write(session[item]+'|')
			csv.write('\n');
			ssend = False

			

log.close

#for item in session:
#	csv.write(item+'|')
#csv.write('\n')
#for dic in sessions:
#	#print(dic)
#	for item in dic:
#		csv.write(dic[item]+'|')
#	csv.write('\n');
	
csv.close
