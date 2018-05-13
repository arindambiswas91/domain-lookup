import requests
import sys
import pymysql
from lxml import html
import time
import gc
import json
from stem import Signal
from stem.control import Controller

headers={'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}


def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

# signal TOR for a new connection 
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="1234")
        controller.signal(Signal.NEWNYM)

def get_tree(url,session):
	r=session.get("https://domainbigdata.com/"+url,verify=False,timeout=30,headers=headers)
	tree=html.fromstring(r.content)
	return tree

def get_name(tree):
	name=""
	name=tree.xpath("//tr[@id='trWordsInDomainName']/td[2]/text()")
	#print(name[0])
	if name:
		return name[0].strip()
	else:
		return "NULL"

def get_ipgeo(tree):
	ip_location=""
	ip_location=tree.xpath("//tr[@id='trIPGeolocation']/td[2]/text()")
	#print(ip_location[0])
	if ip_location:
		return ip_location[0].strip()
	else:
		return "NULL"

def get_registrant_name(tree):
	registrant_name=""
	registrant_name=tree.xpath("//tr[@id='trRegistrantName']/td[2]/a/text()")
	#print(registrant_name[0])
	if registrant_name:
		return registrant_name[0].strip()
	else:
		return "NULL"

def get_registrant_org(tree):
	registrant_org=""
	registrant_org=tree.xpath("//tr[@id='MainMaster_trRegistrantOrganization']/td[2]/text()")
	#print(registrant_org[0])
	if registrant_org:
		return registrant_org[0].strip()
	else:
		return "NULL"

def get_registrant_email(tree):
	registrant_email=""
	registrant_email=tree.xpath("//tr[@id='trRegistrantEmail']/td[2]/a/text()")
	#print(registrant_email[0])
	if registrant_email:
		return registrant_email[0].strip()
	else:
		return "NULL"

def get_registrant_address(tree):
 	registrant_address=""
 	registrant_address=tree.xpath("//tr[@id='trRegistrantAddress']/td[2]/text()")
 	#print(registrant_address[0])
 	if registrant_address:
 		return registrant_address[0].strip()
 	else:
 		return "NULL"

def get_registrant_city(tree):
	registrant_city=""
	registrant_city=tree.xpath("//tr[@id='trRegistrantCity']/td[2]/text()")
	#print(registrant_city[0])
	if registrant_city:
		return registrant_city[0].strip()
	else:
		return "NULL"

def get_registrant_state(tree):
	registrant_state=""
	registrant_state=tree.xpath("//tr[@id='trRegistrantState']/td[2]/text()")
	#print(registrant_state[0])
	if registrant_state:
		return registrant_state[0].strip()
	else:
		return "NULL"

def get_registrant_country(tree):
	registrant_country=""
	registrant_country=tree.xpath("//tr[@id='trRegistrantCountry']/td[2]/text()")
	#print(registrant_country[0])
	if registrant_country:
		return registrant_country[0].strip()
	else:
		return "NULL"

def get_registrant_phone(tree):
	registrant_phone=""
	registrant_phone=tree.xpath("//tr[@id='trRegistrantTel']/td[2]/text()")
	#print(registrant_phone[0])
	if registrant_phone:
		return registrant_phone[0].strip()
	else:
		return "NULL"

def domain_lookup(tree,url):
	with open("output/"+url+".txt",'w',encoding="utf-8") as file:
		name=get_name(tree)
		ip_location=get_ipgeo(tree)
		registrant_name=get_registrant_name(tree)
		registrant_org=get_registrant_org(tree)
		registrant_email=get_registrant_email(tree)
		registrant_address=get_registrant_address(tree)
		registrant_city=get_registrant_city(tree)
		registrant_state=get_registrant_state(tree)
		registrant_country=get_registrant_country(tree)
		registrant_phone=get_registrant_phone(tree)
		result={'domain':url,'name':name,'ip_location':ip_location,'registrant_name':registrant_name,'registrant_org':registrant_org,'registrant_email':registrant_email,'registrant_address':registrant_address,'registrant_city':registrant_city,'registrant_state':registrant_state,'registrant_country':registrant_country,'registrant_phone':registrant_phone}
		print(result)
		json.dump(result,file)
		file.close()
		gc.collect()

if __name__ == '__main__':
	#url="64clicks.com"
	url=sys.argv[1]
	renew_connection()
	time.sleep(10)
	session = get_tor_session()
	tree=get_tree(url,session)
	if tree is not None:
		domain_lookup(tree,url)













