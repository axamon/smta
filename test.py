# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:40:27 2016

@author: 00246506
"""
from scapy.all import TCP, IP, sniff
from scapy_http import http
import redis

rlocal = redis.StrictRedis(host='vocvideo.ddns.net')

def update_stats(context, value, type='test'):
        destination = 'stats:%s:%s'%(context, type)
        #rlocal.lpush(destination+':tempi', value)
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

def process_tcp_packet(packet):
    '''
    Sniffa il traffico e recupera la richiesta del manifest
    '''
    #if not packet.haslayer(http):
    #   return
    try:
            if packet.haslayer(http.HTTPRequest):
                http_layer = packet.getlayer(http.HTTPRequest)
		print http_layer.summary
                ip_layer = packet.getlayer(IP)
                tcp_layer = packet.getlayer(TCP)
                global request
                request = 'http://{1[Host]}{1[Path]}'.format(ip_layer.fields, http_layer.fields)
                global idvideoteca
                try:
                        idvideoteca = str(request.split("/")[8])
                except:
                        pass
                global requestwindow
                requestwindow = '{[window]}'.format(tcp_layer.fields)
                global requestack
                requestack = '{[ack]}'.format(tcp_layer.fields)
                global requesttime
                requesttime = float(packet.time)
                #print requestack, packet.time, tcpwindow, request
                #print packet.show()
                
            if packet.haslayer(http.HTTPResponse):
                http_layer = packet.getlayer(http.HTTPResponse)
                ip_layer = packet.getlayer(IP)
                tcp_layer = packet.getlayer(TCP)
                response = '{1[Status-Line]}'.format(ip_layer.fields, http_layer.fields).split()[1]
                tcpwindow = '{[window]}'.format(tcp_layer.fields)
                responseseq = '{[seq]}'.format(tcp_layer.fields)
                if requestack == responseseq:
                        tts = float(packet.time)-requesttime
                        print idvideoteca, request, tts, requestwindow, response
                        try:
                                update_stats(idvideoteca,tts)
                        except:
                                pass
                #print packet.show()
    except:
                pass
            
sniff(filter='tcp and port 80', prn=process_tcp_packet, store=0)
