import socket
import pickle
import time
import re
import threading
import random

CLOSE_SOCKET_MSG = "!CLOSE_SOCKET!"

def handleTCPClient(clientSocket, clientAddress):
    global STATE

    def downloadFile(path):
        with clientSocket:
            with open(path, "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                    clientSocket.sendall(pdf_data)
                
        print(f"[{clientAddress}] | File Sent Successfully")

    print(f"[NEW SOCKET CONNECTION] {clientAddress} connected.")

    connected = True
    while connected:
        msg = clientSocket.recv(1024).decode()

        if msg == CLOSE_SOCKET_MSG:
            print(f"[{clientAddress}] | Client Socket Closed")
            connected = False

        if (msg == "EMILYANDERSON_DentalHistory_11-21-20" 
            or msg == "DUSTINSTONE_BankStatement_3-9-16"):
           downloadFile(f"{msg}.pdf")
        elif (msg == "CRAFTING_GUIDE"):
            time.sleep(random.randint(3, 7))
            downloadFile(f"{msg}.pdf")
        elif (msg == "facebookProfile"):
            time.sleep(random.randint(3, 7))
            profile =   {
                        'name': 'Splinter Smith',
                        'age': 30,
                        'email': 'smith.splinter@gmail.com',
                        'location': 'Dallas, Texas'
                        }
            clientSocket.send(pickle.dumps(profile))
        elif ("emergencySignal" in msg):
            pattern = r"emergencySignal: (.*)"
            problemStatement = re.search(pattern, msg)
            print(f"[{clientAddress}] | Received Emergency Call")
            response = f"Emergency Response Has Received Your Request. Responding According to Message: {problemStatement.group(1)}"
            clientSocket.send(response.encode())
            

def handleUDPClient(IP):
    print("[ACTIVATING UDP SERVICES] UDP Server is starting...")
    serverUDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    serverUDPSocket.bind((IP, 8081))
    print(f"[LISTENING] Server is listening on {IP}: 8081\n")

    connected = True
    while connected:
        data, clientAddress = serverUDPSocket.recvfrom(1024) 
        if data == CLOSE_SOCKET_MSG:
            connected: False

        print(f"Received from {clientAddress}: {data.decode()}") # decode data and print 
        ack = "Hey, this is the server acknowledging the receipt of your data:" + data.decode() # create an acknowledgement
        serverUDPSocket.sendto(ack.encode(), clientAddress) # encode the acknowledgement the send back to client 

if __name__ == "__main__":
    print("[ACTIVATING TCP SERVICES] TCP Server is starting...")
    serverTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    IP = "192.168.40.84" # use IP given by network
    serverAddress = (IP, 8080)
    serverTCPSocket.bind(serverAddress)
    serverTCPSocket.listen(15)
    print(f"[LISTENING] Server is listening on {IP}: 8080\n")

    ###
    # starts udp server
    udpThread = threading.Thread(target=handleUDPClient, args=(IP,))
    udpThread.start()
    
    # starts tcp server
    while True:
        clientSocket, clientAddress = serverTCPSocket.accept()
        thread = threading.Thread(target=handleTCPClient, args=(clientSocket, clientAddress))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")