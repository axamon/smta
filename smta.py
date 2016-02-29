import pyshark
import urllib2
from lxml import etree
from urlparse import urlparse
import redis
rlocal = redis.StrictRedis()

comandodalanciare ='''
tshark -t e tcp port 80 -Tfields -e frame.time_epoch -e tcp.stream -e http.request.full_uri -e http.response.code -e http.content_type -e http.content_length -b duration:5 -b files:5 -w test2.pcap
'''

def sniffa(log):
    while True:
        #log = "test2_00008_20160226164204.pcap"
        log = rlocal.brpop('listapcap',0)[1]
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
    idvideoteca = url.split("/")[8]
    # print idvideoteca
    if rlocal.exists(idvideoteca) is False:
        print "rompo le palle a videoteca"
        m = url.split("ism")[0]
        manifesturl = m+"ism/manifest"
        request = urllib2.Request(manifesturl)
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
