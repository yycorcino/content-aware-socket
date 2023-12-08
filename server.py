import socket
import pickle
import time
import re
import threading
import random

CLOSE_SOCKET_MSG = "!CLOSE_SOCKET!"

def downloadFile(path, clientSocket):
    """
    handles converting pdf to bytes to send to socket requestor
    """

    with clientSocket:
        with open(path, "rb") as pdf_file:
            pdf_data = pdf_file.read()

            # verifies that the socket isn't closed
            if clientSocket.fileno() != -1:
                clientSocket.sendall(pdf_data) 
                
        print(f"[{clientAddress}] | File Sent Successfully")

def handleTCPClient(clientSocket, clientAddress):
    """
    instance of TCP server to handle TCP client
    """

    print(f"[NEW SOCKET CONNECTION] {clientAddress} connected.")

    connected = True
    while connected:
        msg = clientSocket.recv(1024).decode()

        if msg == CLOSE_SOCKET_MSG:
            print(f"[{clientAddress}] | Client Socket Closed")
            connected = False

        if (msg == "EMILYANDERSON_DentalHistory_11-21-20" 
            or msg == "DUSTINSTONE_BankStatement_3-9-16"):
           downloadFile(f"{msg}.pdf", clientSocket)
        elif (msg == "CRAFTING_GUIDE"):
            time.sleep(random.randint(3, 7))
            downloadFile(f"{msg}.pdf", clientSocket)
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
            
if __name__ == "__main__":
    print("[ACTIVATING TCP SERVICES] TCP Server is starting...")
    serverTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    IP = "192.168.1.113" # use IP given by network
    serverTCPSocket.bind((IP, 8080))
    serverTCPSocket.listen(15) # max 15 clients
    print(f"[LISTENING] Server is listening on {IP}: 8080\n")
    
    # starts tcp server on a thread and connect instance of server to a client
    while True:
        clientSocket, clientAddress = serverTCPSocket.accept()
        threading.Thread(target=handleTCPClient, args=(clientSocket, clientAddress)).start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")