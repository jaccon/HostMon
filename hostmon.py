# NETWORK SCAN MANANGER 
# Update 20/09/2013
# by @jaccon - jaccon@gmail.com

import subprocess
import os
import datetime
import sys
import re
import commands
import smtplib

# SET CONFIGURATION FILE
config_file='hosts.conf'
log_file='hosts.log'
cache_file='cache/temp.log'

# SET MAIL CONFIGURATION
send_to="YOUR-EMAIL-HERE"
send_subject="BLUE SYSTEMS HOSTS MONITOR"
smtp_server="YOUR-SMTP-SERVER-HERE"
smtp_port="SMTP-TCP-PORT"
smtp_login="YOUR-EMAIL-USER-LOGIN"
smtp_login_password="YOUR-EMAIL-USER-PASSWORD"

# SMS SETTINGS
sms_enable="0"
sms_subject_number="YOUR-CELLPHONE-NUMBER"
sms_forward_mail="YOUR-EMAIL-TO-GET-CELLPHONE"

# HEADER
CSI="\x1B["
linkDown=CSI+"31;40m" + " DOWN " + CSI + "0m" + CSI + "0m"
linkUP=CSI+"32;40m" + " UP " + CSI + "0m" + CSI + "0m"
headerFile=CSI+"33;40m" + " BLUE SYSTEMS HOSTS MONITOR " + CSI + "0m" + CSI + "0m"
get_messages="TESTE"

# clean cache content
fcache = open(cache_file,'r+')
fcache.truncate()

# clean screen
f = open(config_file)
ip = f.readline()
os.system('clear')
print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=---=-=="
print "-  "+ headerFile +"-"
print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-="
print " "

with open(os.devnull, "wb") as limbo:
    while ip:
	ip=ip.replace(" ","")
	ip = re.sub(r"\s+",'',ip)
	ipaddr=(ip.split(":")[0])
	hostname=(ip.split(":")[1])
	critical=(ip.split(":")[2])
	
	# critival level
	if critical == "C":
	  critical_level="critico"
	elif critical == "D":
	  critical_level="default" 
	
	# send a ICMP packet 
	result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ipaddr],
            stdout=limbo, stderr=limbo).wait()
	if result:
                print "HOST: " + ipaddr + " - " + hostname + " - STATUS: "+ linkDown + " - " + critical_level
                print "TIME: " + str(datetime.datetime.now())
                print "\n"
                # WRITE TO LOGFILE
                with open(log_file, "a") as myfile:
                    myfile.write("\n"+"IP: "+ ipaddr + "- " + hostname +" "+ critical_level + " - STATUS: DOWN "+ "TIME: "+str(datetime.datetime.now()) + "\n" );
                
                # WRITE A CACHE LOGFILE
                with open(cache_file, "a") as myfile2:
                    myfile2.write("\n"+ ipaddr + " - " + hostname + " "+critical_level + " - link down in "+str(datetime.datetime.now()) + "\n" );
		
		# SEND SMS TO CRITICAL HOST
		if sms_enable == "1":
			print "SMS ENABLE"
		sms_message=ipaddr+ " "+hostname+" host down "
                header = ('From: <'+smtp_login+'>\n'
          'To: <'+sms_forward_mail+'>\n'
          'Subject: '+ sms_subject_number +'\n'
          '\n'
          +sms_message+" "+'\n')
                message=header+"---"
                server = smtplib.SMTP(smtp_server,smtp_port)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_login,smtp_login_password)
                server.sendmail(smtp_login,sms_forward_mail,"Subject:"+sms_subject_number+'\n'+sms_message)
                server.rset()
                server.quit()
	else:
                print "HOST: " + ipaddr + " - " + hostname + " - STATUS: "+ linkUP + " - " + critical_level
                print "TIME: " + str(datetime.datetime.now())
                print "\n"
        ip = f.readline()
    f.close()

    # SEND MAIL NOTIFICATION
    print "[+] SEND MAIL NOTIFICATIONS [+]"
    print ""

    f = open(cache_file,"r")
    msg_filename = f.read()

    header = ('From: <'+smtp_login+'>\n'
        'To: <'+send_to+'>\n'
        'Subject: '+send_subject+'\n'
        '\n'
        +msg_filename+'\n')

    message=header+"---"
    server = smtplib.SMTP(smtp_server,smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtp_login,smtp_login_password)
    server.sendmail(smtp_login,send_to,message)
    server.rset()
    server.quit()
