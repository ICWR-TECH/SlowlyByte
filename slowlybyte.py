#!/usr/bin/python
# SlowlyByte - Web Server
# Version 1.0 ( Alpha )
# Copyright (c)2019 - Afrizal F.A - IN CRUST WE RUSH

import os, re, sys, socket, urllib

port=int(sys.argv[1])

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", port))
s.listen(True)

while True :
	c,a=s.accept()
	data=c.recv(1024)
	line_headers=data.split("\n")
	print(data)
	open_file=re.findall("/(.+?) HTTP/" ,line_headers[0])
	if not open_file :
		if os.path.isfile("index.html") :
			open_file=["index.html"]
		if os.path.isfile("index.php") :
			open_file=["index.php"]
	if open_file :
		inputopen=urllib.unquote(open_file[0])
		split_ext=inputopen.split(".")[-1]
	else :
		content_type="text/html"
	if str(split_ext) :
		if str(split_ext) == "html" or str(split_ext) == "php" or str(split_ext) == "phtml" :
			content_type="text/html"
		elif str(split_ext) == "txt" or str(split_ext) == "css" or str(split_ext) == "js":
			content_type="text/plain"
		elif str(split_ext) == "mp4" :
			content_type="video/mp4"
		elif str(split_ext) == "mp3" :
			content_type="audio/mp3"
		else :
			content_type="application/octet-stream"
	else :
		content_type="text/html"
		
	h_ok="""\nHTTP/1.1 200 OK\nServer: SlowlyByte ( IN CRUST WE RUSH )\nConnection: Close\nContent-Type: %s\n\n"""%(content_type)
	h_notfound="""\nHTTP/1.1 404 Not Found\nServer: SlowlyByte ( IN CRUST WE RUSH )\nConnection: Close\nContent-Type: text/html\n\n404 Not Found"""
	try :
		if open_file :
			if os.path.isfile(inputopen) :
				file_content=open(inputopen, "r").read()
				c.sendall(h_ok+file_content)
			elif os.path.isdir(inputopen) :
				if os.path.isfile(inputopen+"/index.html") :
					open_file=[inputopen+"/index.html"]
				if os.path.isfile(inputopen+"/index.php") :
					open_file=[inputopen+"/index.php"]
				c.sendall("HTTP/1.1 200 OK\nServer: SlowlyByte ( IN CRUST WE RUSH )\nConnection: Close\nContent-Type: text/html\n\n"+open(inputopen, "r").read())
			else :
				c.sendall(h_notfound)
		else :
			c.sendall(h_notfound)
	except :
		pass
