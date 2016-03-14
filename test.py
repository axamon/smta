from scapy.all import TCP, IP, sniff
from scapy_http import http

def process_tcp_packet(packet):
    '''
    Sniffa il traffico e recupera la richiesta del manifest
    '''
    #if not packet.haslayer(http.HTTPRequest):
#	return
    if packet.haslayer(http.HTTPRequest):
    	http_layer = packet.getlayer(http.HTTPRequest)
    	ip_layer = packet.getlayer(IP)
	tcp_layer = packet.getlayer(TCP)
    	request = '{1[Host]}{1[Path]}'.format(ip_layer.fields, http_layer.fields)
	tcpwindow = '{[window]}'.format(tcp_layer.fields)
	requestack = '{[ack]}'.format(tcp_layer.fields)
    	print requestack, packet.time, tcpwindow, request
	#print packet.show()

    if packet.haslayer(http.HTTPResponse):
    	http_layer = packet.getlayer(http.HTTPResponse)
    	ip_layer = packet.getlayer(IP)
	tcp_layer = packet.getlayer(TCP)
    	response = '{1[Status-Line]},{2[window]}'.format(ip_layer.fields, http_layer.fields, tcp_layer.fields)
	tcpwindow = '{[window]}'.format(tcp_layer.fields)
	responseseq = '{[seq]}'.format(tcp_layer.fields)
    	print responseseq, packet.time, tcpwindow, response
	#print packet.show()

    #if packet.haslayer(TCP):
#	tcp_layer = packet.getlayer(TCP)
#    	ip_layer = packet.getlayer(IP)
##	tcpwindow = '{[window]}'.format(tcp_layer.fields)
##	print tcpwindow

sniff(filter='tcp and port 80', prn=process_tcp_packet, store=0)
