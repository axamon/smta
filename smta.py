import time
import os
import pyshark
import urllib2
from lxml import etree
#from urlparse import urlparse
import requests
import redis
rlocal = redis.StrictRedis()
#from scapy.all import IP, sniff
#from scapy_http import http

comandodalanciare ='''
tshark -t e tcp port 80 -Tfields -e frame.time_epoch -e tcp.stream -e http.request.full_uri -e http.response.code -e http.content_type -e http.content_length -b duration:5 -b files:5 -w test2.pcap
'''


def start(idunivoco):
    'riceve un idunivoco di fruizione e comincia lo sniff'
    from scapy.all import wrpcap, sniff
    rlocal.set(idunivoco+"_status",'running')
    i = 0
    while True:
        p= sniff(filter='tcp port 80', iface='eth0', timeout=30)
        i=i+1
        filepcap = idunivoco+"_"+str(i)+'.pcap'
        wrpcap(filepcap,p)
        rlocal.lpush(idunivoco+"_files",filepcap)
        if rlocal.get(idunivoco+"_status") == 'stop':
            break
        
def stop(idunivoco):
    'interrompe lo sniffing'
    rlocal.set(idunivoco+"_status",'stop')
    
def elabora(idunivoco):
    while True:
        filepcap = rlocal.brpop(idunivoco+"_files",0)[1]
        print filepcap
        os.system('/root/pcap2har/main.py '+filepcap+" "+filepcap+".har")
        if int(rlocal.llen(idunivoco+"_files")) == 0:
            break    

def sniffa():
	sniff(filter='tcp', prn=process_tcp_packet, timeout=20)
	return url

def process_tcp_packet(packet):
    '''
    Sniffa il traffico e recupera la richiesta del manifest
    '''
    if not packet.haslayer(http.HTTPRequest):
        # This packet doesn't contain an HTTP request so we skip it
        return
    http_layer = packet.getlayer(http.HTTPRequest)
    ip_layer = packet.getlayer(IP)
    request = '{1[Host]}{1[Path]}'.format(ip_layer.fields, http_layer.fields)
    #print request
    if 'anifest' in request:
	#print request
	global url
	url = 'http://'+request
	#caricamanifest(url)
	return

def scarica(url):
	'''Scarica tutti i chunk di un film al massimo livello'''
	idvideoteca = url.split("/")[8]
	t=0
	num=0
	numchunks = int(rlocal.hget(idvideoteca,'chunks'))
	maxlevel = int(rlocal.hget(idvideoteca,'qualitylevels'))-1
	maxbitrate = str(rlocal.hget(idvideoteca,maxlevel))
	#urlbase = url.split("manifest")[0]+"QualityLevels("+maxbitrate+")/Fragments(video="+str(t)+")"
	while num < numchunks:
		num = num + 1
        	#chunk = "http://vodabr.cb.ticdn.it/videoteca2/V3/Film/2014/04/50403788/SS/10422185/10422185.ism/QualityLevels(5500000)/Fragments(video="+str(t)+")"
		chunk = url.split("Manifest")[0]+"QualityLevels("+maxbitrate+")/Fragments(video="+str(t)+")"
		print chunk
        	response = requests.get(chunk)
        	print response.status_code, response.elapsed.total_seconds(), float(response.headers['Content-Length'])/1024/response.elapsed.total_seconds()/1024, response.headers['VT3'], response.url.split("/")[2]
        	print response.headers
        	tts = float(response.elapsed.total_seconds())
        	print tts
        	update_stats(idvideoteca, tts)
        	t=t+20000000
        	#time.sleep(1)


def update_stats(context, value, type='test'):
        destination = 'stats:%s:%s'%(context, type)
        rlocal.lpush(destination+':tempi', value)
        rlocal.hsetnx(destination, 'min', value)
        rlocal.hsetnx(destination, 'max', value)
        if value < float(rlocal.hget(destination, 'min')):
                rlocal.hset(destination, 'min', value)
        if value > float(rlocal.hget(destination, 'max')):
                rlocal.hset(destination, 'max', value)
        count = int(rlocal.hincrby(destination, 'count',1))
        sum = float(rlocal.hincrbyfloat(destination, 'sum', value))
        sumq = float(rlocal.hincrbyfloat(destination, 'sumq', value*value))
        avg = sum/count
        stddev = float(((sumq / count) - (avg ** 2)) ** .5)
        rlocal.hset(destination,'avg',avg)
        rlocal.hset(destination,'stddev',stddev)


def sniffaold(log):
    while True:
        #log = "test2_00008_20160226164204.pcap"
        if int(rlocal.llen('listapcap')) > 1:
                log = rlocal.rpop('listapcap')
        else:
            time.sleep(5)
            pass
        print log
        try:
            cap = pyshark.FileCapture(log)
            for pacchetto in cap:
                #url = pacchetto.http.request_full_uri
                #print pacchetto.sniff_timestamp, pacchetto.http.request_full_uri, pacchetto.http.response_code
                #rlocal.hmset('log','date',str(pacchetto.sniff_timestamp),'url',str(pacchetto.http.request_full_uri))
                #print pacchetto.http.request_full_uri
                date = pacchetto.sniff_timestamp
                url = pacchetto.http.request_full_uri
                #print url
                if "video" in url:
                    idvideoteca = url.split("/")[8]
                    caricamanifest(url)
                    ql = url.replace('(','/').replace(')','/').split("/")[13]
                    level = rlocal.hget(idvideoteca,ql)
                    print level
                    rlocal.hincrby("fruizione:"+idvideoteca,"qoe",level) #aumenta del livello fruito il contatore
                    rlocal.hincrby("fruizione:"+idvideoteca,"cvf",1) #aumenta di uno i chunk video fruiti cvf
                    qoenav = int(rlocal.hget("fruizione:"+idvideoteca,"qoe"))
                    #print qoe
                    cvf = int(rlocal.hget("fruizione:"+idvideoteca,"cvf"))
                    #print cvf
                    #qoenav = int(qoe)*int(cvf)
                    print qoenav
                    maxliv = int(rlocal.hget(idvideoteca,"qualitylevels"))-1
                    qoemax = maxliv * cvf
                    print qoemax
                    qoeatt = float(qoenav)/float(qoemax)
                    print qoeatt
                    #print date, url
                    #rlocal.hmset('navigazione','date',date,'url',url,'ql',ql)
                    #rlocal.hmset('log5','date',int(pacchetto.sniff_timestamp),'url',str(pacchetto.http.request_full_uri))
                    #print pacchetto.http.response_code
                    #print pacchetto.tcp.flags_reset
        except:
                pass


def caricamanifest(url):
    #url = "http://se-mi1-5.se.vodabr.cb.ticdn.it/videoteca2/V3/SerieTV/2015/10/50521039/SS/10756324/10756324_TV_HD.ism/manifest"
    print url
    idvideoteca = url.split("/")[8]
    print idvideoteca
    if rlocal.exists(idvideoteca) is False:
        print "rompo le palle a videoteca"
        #m = url.split("ism")[0]
        #manifesturl = m+"ism/manifest"
        request = urllib2.Request(url)
        rawPage = urllib2.urlopen(request)
        manifest = rawPage.read()
        tree = etree.XML(manifest)
        rlocal.hset(idvideoteca,"duration",int(tree.xpath('/SmoothStreamingMedia')[0].attrib['Duration']))
        rlocal.hset(idvideoteca,"qualitylevels",int(tree.xpath('/SmoothStreamingMedia/StreamIndex')[0].attrib['QualityLevels']))
        rlocal.hset(idvideoteca,"chunks",int(tree.xpath('/SmoothStreamingMedia/StreamIndex')[0].attrib['Chunks']))
        r = tree.xpath('/SmoothStreamingMedia/StreamIndex/QualityLevel')
        #print len(r)
        for i in range(len(r)):
            #print r[i].attrib
                #per escludere audio prendo solo bitrate elevati
            if int(r[i].attrib['Bitrate']) > 250000:
                #rlocal.set(idvideoteca+":livellovideo"+r[i].attrib['Index'], int(r[i].attrib['Bitrate']))
                #crea un hash in redis con idvideoteca il bitrate e il livello associato
                rlocal.hset(idvideoteca, int(r[i].attrib['Bitrate']), int(r[i].attrib['Index']))
                rlocal.hset(idvideoteca, int(r[i].attrib['Index']), int(r[i].attrib['Bitrate']))
    return
