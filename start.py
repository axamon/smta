import os
import sys
import redis
rlocal = redis.StrictRedis()

def start(idunivoco):
    'riceve un idunivoco di fruizione e comincia lo sniff'
    from scapy.all import wrpcap, sniff
    rlocal.set(idunivoco+"_status",'running')
    #elabora(idunivoco)
    i = 0
    while True:
        p= sniff(filter='tcp port 80', iface='eth0', timeout=30)
        i=i+1
        filepcap = idunivoco+"_"+str(i)+'.pcap'
        wrpcap(filepcap,p)
        rlocal.lpush(idunivoco+"_files",filepcap)
        if rlocal.get(idunivoco+"_status") == 'stop':
	    sys.exit("Cattura fruizione "+idunivoco+" finita")
            break
        
def stop(idunivoco):
    'interrompe lo sniffing'
    rlocal.set(idunivoco+"_status",'stop')
 
def elabora(idunivoco):
    while True:
        filepcap = rlocal.brpop(idunivoco+"_files",0)[1]
        print filepcap
        os.system('/root/pcap2har/main.py '+filepcap+" "+filepcap+".har")
	os.remove(filepcap)
        if int(rlocal.llen(idunivoco+"_files")) == 0:
            break
    
    
    
    
