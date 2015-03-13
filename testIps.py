#!/usr/bin/python

import os
import sys
import re

 
HOME = os.environ['HOME']
ips_dir = os.path.join(HOME,"Documents/IPS_TEST_RESULT")

class Log(object):
    def __init__(self,*args,**kargs):
        sys.stdout.flush()

    count = 0
    tags = {
            0:"-",
            1:"\\",
            2:"|",
            3:"/",
    }

    def log(self,content):
        tag = Log.tags[Log.count % 4]
        sys.stdout.flush()
        content = self.concate(30,content)
        sys.stdout.write("%30ls\t\t%s\r"%(content,tag))
        Log.count += 1
    def concate(self,num,string,sub=" "):
        if len(string) < num:
            new_string = string + sub*(num - len(string))
            return new_string
        return new_string
    def right_concate(self,num,sub="#",all_num=20):
        return sub* (all_num -num) +  " "*num +" | " +str(all_num - num)
    def draw_result(self,time,tab,sub_core,scale):
        num = int(sub_core/scale) 
        print "%20s :%20s [%8f ms]"%(self.concate(35,tab) ,self.right_concate(num),time )

loger = Log()
def getIps(file_path):
    with file(file_path,"r") as fp:
        txt = fp.readlines()
        ips = [ip.strip() for ip in txt]

        return ips



def testOneIp(ip,ips_dir,time="4"):

    if os.path.exists(ips_dir):
        ip_dir = os.path.join(ips_dir,ip)
    else :
        os.mkdir(ips_dir)
        ip_dir = os.path.join(ips_dir,ip)

    command = "echo '312211dark' | sudo -S ping -c %s -i 0.1 %s | grep time= | awk '{ print  $7 }' > %s.result "%(time,ip,ip_dir )
     
    os.popen (command)
    loger.log(ip)

def getResult(result_dir):
    files = [ os.path.join(result_dir,name.strip()) for name in  os.listdir(result_dir)]
    int_re = re.compile(r'[\d\.]+')
    def get_core(file_name):
        return  int_re.findall(file(file_name).read())

    core = [ [float(i) for i in get_core(file_path) ] for file_path in files]
    keys = [file_name.split("/")[-1] for file_name in files]
    keys = [ ".".join(ip.split(".")[:-1]) for ip in keys]
    res =  dict(zip(keys,core ))
    return res
def drawResult(cores):
    aves = [ sum(cores[core])/float( len(cores[core])) for core in cores ]
    max_core  =  max(aves)
    min_core = min(aves)
    each_sub = [  x - min_core for x in aves ]
    sub_hash = dict(zip(cores.keys(),each_sub))

    scale =( max_core - min_core) /20

    [loger.draw_result(cores[sub_core_key][0],sub_core_key,sub_hash[sub_core_key],scale) for sub_core_key in sub_hash]




def main(ips_file,time="4"):
    ips = getIps(ips_file)
    map(testOneIp,ips,[ips_dir for i in ips],[time for i in ips])
    cores = getResult(ips_dir)
    drawResult(cores)

if __name__ =="__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1],sys.argv[2])
    elif len(sys.argv) == 1:
        main("~/Documents/server.list")
    else:
        print "argu error"
        print "testIps.py ~/xxx/some.ips [time]"
