#!/bin/env python
#coding:utf-8

import time,sys,getopt

blue = '\033[36m'
yellow = '\033[33m'
red = '\033[32m'
flicker = '\033[5m'
closeAttribute = '\033[0m'


def usage():
        """
The output  configuration file contents.

Usage: config.py [-d|--domain,[number|'m']] [-c|--cache,[allow|deny]]

Description
        -d,--domain     generate domain configuration,take 13 or 19 number,"m" is the second - tier cities.
        -c,--cache      configure cache policy. "allow" or "deny".
for example:
        python config.py -d 13
        python config.py -c allow
"""


def separator(sepa=None):
	s = "-"*70
	print '%s%s%s %s %s%s' % (flicker,blue,s,sepa,s,closeAttribute)

#print '\n\033[36m'+'cnc'.center(120,'-')+'\033[0m\n'


def colors(doc='content'):
	print '%s%s%s%s' % (flicker,yellow,doc,closeAttribute)


class DefCurrentConf(object):
	def __init__(self):
		self.curtime = time.strftime('%Y-%m-%d',time.localtime())
		self.curdate = time.strftime('%Y%m%d',time.localtime())
		self.monlink_uri = "/do_not_delete/noc.gif"
		self.cache_type = "jpg|jpeg|gif|png|swf|js|css"
		self.defdomainconf_13 = '%s N Y 1 0.001 0.6 20000 1 Y no GET:%s%s  2**|3**|404  %s'
		self.defdomainconf_19 = '%s N Y 1 0.001 0.6 20000 1 Y no GET:%s%s 2**|3**|404 %s GET:%s%s %s N 100:0 3 Y'
		self.defdomainconf_secondary = '%s N Y 1 0.001 0.6 20000 1 Y no GET:%s%s  2**|3**|404  %s|%s'
		try:
			with open('channel.txt') as f:
				self.name = f.readline()
				self.namedef = self.name.split()[-1]
				f.seek(0)
				self.list1 = f.readlines()
		except IOError:
			colors("Could not open channel.txt:No such file or directory")
			exit()
	def domain_start(self):
		print '\n#%s %s start' % (self.namedef,self.curtime)
	def domain_end(self):
		print '#%s %s end\n' % (self.namedef,self.curtime)

class CreateProfile(DefCurrentConf):
	def __init__(self):
		super(CreateProfile,self).__init__()
		

	def domain(self,number=13):
		'''13项配置。
		
		注意，这是通用的13项配置，请认真检查其正确性并酌情修改！'''
		if number == 13:
			self.domain_start()
			for i in self.list1:
				list2 = i.split()
				domain = list2[0]
				srcipadd = list2[1]
				print self.defdomainconf_13  % (domain,domain,self.monlink_uri,srcipadd)
			self.domain_end()
	#def domain_19(self):
#		'''19项配置。
#	
#		注意，这是通用的19项配置，适用于特殊端口配置，请认真检查其正确性并酌情修改！'''
		elif number == 19:
			self.domain_start()
			for i in self.list1:
				list2 = i.split()
				domain = list2[0]
				portnum = list2[2]
				srcipadd = list2[1]
				print self.defdomainconf_19  % (domain,domain,self.monlink_uri,srcipadd,domain,self.monlink_uri,portnum)
			self.domain_end()
	def secondaryCity(self):
		self.zzchn = '61.164.60.161|114.80.101.140|220.181.65.36|119.147.113.21'
		self.zzcnc = '58.68.142.206|112.90.217.109'
		self.zzcmn = '58.68.238.77'

		separator('CHN')
		self.domain_start()
		for i in self.list1:
			list2 = i.split()
			domain = list2[0]
			srcipadd = list2[1]
			print self.defdomainconf_secondary %  (domain,domain,self.monlink_uri,srcipadd,self.zzchn)
		self.domain_end()

		separator('CNC')
		self.domain_start()
		for i in self.list1:
        	        list2 = i.split()
                	domain = list2[0]
	                srcipadd = list2[1]
			print self.defdomainconf_secondary %  (domain,domain,self.monlink_uri,srcipadd,self.zzcnc)
		self.domain_end()

		separator('CMN')
		self.domain_start()
		for i in self.list1:
			list2 = i.split()
			domain = list2[0]
			srcipadd = list2[1]
			print self.defdomainconf_secondary  %  (domain,domain,self.monlink_uri,srcipadd,self.zzcmn)
		self.domain_end()
	def cache(self,policy="allow"):
		if policy == "allow":
			print "\n"
			for i in self.list1:
				list2 = i.split()
				domain = list2[0]
				nocachename = '%s%s_nocache' % (domain,self.curdate)
				cachename = '%s%s_cache' % (domain,self.curdate)
				refreshtime = int(list2[2])
				print '#<%s' % (domain)
				print 'acl %s dstdomain %s' % (nocachename,domain)
				print 'acl %s url_regex -i ^http://%s/.*\.(%s)(@@@|$|\?)' % (cachename,domain,self.cache_type)
				print 'cache allow %s' % (cachename)
				print 'cache deny %s' % (nocachename)
				print 'refresh_pattern -i @http://%s/.*\.(%s)(@@@|$|\?) %s 0%% %s ignore-reload override-lastmod' % (domain,self.cache_type,refreshtime,refreshtime)
				print '#>%s' % (domain)
			print "\n" 
		elif policy == "deny":
			print ""
			for i in self.list1:
				list2 = i.split()
				domain = list2[0]
				nocachename = '%s%s_nocache' % (domain,self.curdate)
				print '#<%s' % (domain)
				print 'acl %s dstdomain %s' % (nocachename,domain)
				print 'cache deny %s' % (nocachename)
				print '#>%s' % (domain)
			print ""

ttt=CreateProfile()
#ttt.domain(13)

if __name__ == "__main__":
#	try:
#		options = raw_input("请选择要生成的配置内容[domainconf_13|domainconf_19|cache_allow|cache_deny]：").strip()
#	except (KeyboardInterrupt,EOFError,NameError):
#		print ''
#		exit()	
#	else:
#		if options == ('domain_13' or 'd13'):
#			print "d13"
#			ttt.domain_13()
#		elif options in ('domain_19','d19'):
#			ttt.domain_19()
#		elif options == 'cache_allow':
#			ttt.cache_allow()
#		elif options == "secondary cities":
#			ttt.secondaryCity()
#		elif options == 'cache_deny':
#			ttt.cache_deny()
	#finally:
	#	pass

#def getopttest():
        try:
                options,args = getopt.getopt(sys.argv[1:],"d:c:vh",["help","output="])
        except getopt.GetoptError as err:
                print str(err)
                usage()
                sys.exit(1)
        #output = None
        #verbose = False
        for o,a in options:
	#for b in args:		# Value other than args agruments for getopt format.

                if o in ("-d") and a in ("13"):
			ttt.domain(int(a))
		elif o in ("-d") and a in ("19"):
			ttt.domain(int(a))
		elif o in ("-c","--cache") and a in ("allow"):
			ttt.cache("allow")
		
                elif o in ("-h","--help"):
                        #usage()
                        print usage.__doc__
                        sys.exit()
                elif o in ("-o","--output"):
                        output = a
                else:
#			assert False, "unhandled option."
			print 0












