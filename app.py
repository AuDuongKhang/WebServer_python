import socket
import os
from os import error
import threading


#Create ip and port server
#HOST = socket.gethostbyname(socket.gethostname())
HOST = "localhost"
PORT = 8080

#Create socket server
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    SERVER.bind(('',PORT))
    print(f'* Running on http://{HOST}:{PORT}')
except socket.error as e:
    print(f'socket error: {e}')
    print('socket error: %s' %(e))

#Start the server
def _start():
    SERVER.listen(5)
    while True: 
        conn, addr = SERVER.accept()
        thread = threading.Thread(target=_handle, args=(conn, addr))
        thread.start()


#Receive request from client and response to client
def _handle(conn,addr):
    conn.settimeout(5)
    while True:
        data = conn.recv(1024).decode()                         #decode the request into string
        if not data: break
        
        #split request to request method and request url
        request_line = data.split('\r\n')[0]                    
        request_method = request_line.split(' ')[0]
        reuqest_url = (request_line.split(' ')[1]).strip('/')
        
        #if request method is 'GET', render file with the following request url
        if request_method == 'GET':                                                        
            if reuqest_url == '':                             
                #index page
                url = 'index.html'
                Content_type = 'text/html'
            elif reuqest_url == 'index.html':             
                url = reuqest_url
                Content_type = 'text/html'
            elif reuqest_url == 'favicon.ico':             
                url = reuqest_url
                Content_type = 'image/x-icon'
            elif reuqest_url == 'css/style.css':           
                url = reuqest_url
                Content_type = 'text/css'
            elif reuqest_url == 'css/utils.css':           
                url = reuqest_url
                Content_type = 'text/css'
            elif reuqest_url == 'avatars/1.png':            
                url = reuqest_url
                Content_type = 'image/png'
            elif reuqest_url == 'avatars/2.png':
                url = reuqest_url
                Content_type = 'image/png'
            elif reuqest_url == 'avatars/3.png':
                url = reuqest_url
                Content_type = 'image/png'
            elif reuqest_url == 'avatars/4.png':
                url = reuqest_url
                Content_type = 'image/png'
            elif reuqest_url == 'avatars/5.png':
                url = reuqest_url
                Content_type = 'image/png'
            elif reuqest_url == 'avatars/6.png':
                url = reuqest_url
                Content_type = 'image/png'
            elif reuqest_url == 'avatars/7.png':
                url = reuqest_url
                Content_type = 'image/png'
            elif reuqest_url == 'avatars/8.png':
                url = reuqest_url
                Content_type = 'image/png'
            elif reuqest_url == 'image1.jpg':
                url = reuqest_url
                Content_type = 'image/jpeg'
            elif reuqest_url == 'image2.jpg':
                url = reuqest_url
                Content_type = 'image/jpeg'
            elif reuqest_url == 'image3.jpg':
                url = reuqest_url
                Content_type = 'image/jpeg'
            elif reuqest_url == 'image4.jpg':
                url = reuqest_url
                Content_type = 'image/jpeg'
            else:                                           #if the file doesnt exist in server or try to get into images.html
                url = '404.html'                            #without sign in, response is 404 not found.                           
                Content_type = 'text/html'
                data = _read_file_404(url,Content_type)     #write 404 response
                conn.send(data)                             #send data cho client(browser)
                conn.close()                                #close connection
                break
              
            data = _read_file(url,Content_type)             #write normal response
            conn.send(data)                                 #send data cho client(browser)
            conn.close()                                    #close connection
            break
            
        #if request method is 'POST', receive the uname and psw and check them        
        if request_method == 'POST':
            if reuqest_url == 'images.html':
        
        #if they are true, you can see images.html page, else response 401 Unauthorized 
                if _check_pass(data) == True:
                    url = 'images.html'
                    Content_type = 'text/html'
                    data = _read_file(url,Content_type)         #write normal response
                    conn.send(data)                             #send data cho client(browser)
                    conn.close()                                #close connection
                    break
                else:             
                    url = '401.html'
                    Content_type = 'text/html'
                    data = _read_file_401(url,Content_type)     #write 401 response
                    conn.send(data)                             #send data cho client(browser)
                    conn.close()                                #close connection
                    break
        
#Read file and write response header 
def _read_file(Name_file,Content_type):
    f = open(Name_file, 'rb')
    file_stats = os.stat(Name_file)
    fdata = _response_header(file_stats,Content_type)
    fdata += f.read()
    return fdata

#Read file and write response 401 header 
def _read_file_401(Name_file,Content_type):
    f = open(Name_file, 'rb')
    fdata = _response_header_401(Content_type)
    fdata += f.read()
    return fdata

#Read file and write response 404 header 
def _read_file_404(Name_file,Content_type):
    f = open(Name_file, 'rb')
    fdata = _response_header_404(Content_type)
    fdata += f.read()
    return fdata

#Write response header and send to client (browser)
def _response_header(file_stats,Content_type):
    message_header = 'HTTP/1.1 200 OK \r\n'
    message_header += f'Content-type: {Content_type} \r\n'
    message_header += f'Content-length:{file_stats.st_size} \r\n'
    message_header += f'Connection: Closed'
    
    # add 
    message_header += '\r\n\r\n'
    message_header = message_header.encode()
    
    return message_header

#Write response 401 header and send to client (browser)
def _response_header_401(Content_type):
    message_header = 'HTTP/1.1 401 Unauthorized \r\n'
    message_header += f'Content type: {Content_type}'
    # add 
    message_header += '\r\n\r\n'
    message_header = message_header.encode()
    
    return message_header

#Write response 404 header and send to client (browser)
def _response_header_404(Content_type):
    message_header = 'HTTP/1.1 404 Not found\r\n'
    message_header += f'Content type: {Content_type}'
    # add 
    message_header += '\r\n\r\n'
    message_header = message_header.encode()
    
    return message_header

#check uname and psw
def _check_pass(data): 
    if data.find("uname=admin&psw=123456") == -1:
            return False
    else: 
        return True

#main function
if __name__ == '__main__':
    _start()