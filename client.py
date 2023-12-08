import socket
import pickle
import subprocess
import platform

CLOSE_SOCKET_MSG = "!CLOSE_SOCKET!"

# [service name, server command]
availableServices = {   1: ['Retrieve Dental Records', 'EMILYANDERSON_DentalHistory_11-21-20'],
                        2: ['Retrieve Facebook Profile', 'facebookProfile'],
                        3: ['Retrieve Gaming Manual', 'CRAFTING_GUIDE'],
                        4: ['Retrieve Bank Statements', 'DUSTINSTONE_BankStatement_3-9-16'],
                        5: ['Send an Emergency Call', 'emergencySignal'],
                        6: ['End Services', CLOSE_SOCKET_MSG] }

def getChoice():
    """
    get user choice of service and verifies correct input
    """

    print("Available Services: ")
    for index, serviceName in availableServices.items():
        print(f"\t{index}: {serviceName[0]}")
    print("\n")

    while True:
        serviceChoice = input("Please Select One Service From The Following Options (1-6): ")
        if (serviceChoice.isdigit() and  int(serviceChoice) in range(1, 7)):
            return serviceChoice
        else:
            print("Invalid input. Please enter a number between 1 and 6.")
        

def receivePdf(fileName, clientSocket):
    """
    manages client socket stream of bytes which is identified as PDF info
    """

    # read the stream of bytes and convert to human readable text
    pdfData = b""
    while True:
        data = clientSocket.recv(1024)
        if not data:
            break
        pdfData += data

    # human readable text is stored in pdf format
    with open(fileName, "wb") as pdf_file:
        pdf_file.write(pdfData)
    print(f"File Received and Saved as {fileName}")
    
    # opens pdf on user specific system
    system_platform = platform.system()
    if (system_platform == "Darwin"):  
        subprocess.run(["open", fileName], check=True)
    elif (system_platform == "Windows"):
        subprocess.Popen(["start", fileName], shell=True)
    
if __name__ == "__main__":    
    running = True
    while running: 
        command = int(getChoice())
        serverCommand = availableServices[command][1]

        # ask for additional info for emergency call
        if (command == 5):
            additionalMsg = input("What is the Emergency: ")
            serverCommand = serverCommand + ": " + additionalMsg

        IP = '192.168.1.113' # use IP given by network
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((IP, 8080))
        clientSocket.send(serverCommand.encode())

        # logic to handle the incoming data from server
        if (command == 1):
            receivePdf("EMILYANDERSON_DentalHistory_11-21-20.pdf", clientSocket)
        elif (command  == 2): 
            response = clientSocket.recv(1024)
            msg = pickle.loads(response)
            print(f"Here is your Facebook Data: {msg}")
        elif (command == 3):
            receivePdf("CRAFTING_GUIDE.pdf", clientSocket)
        elif (command == 4):
            receivePdf("DUSTINSTONE_BankStatement_3-9-16.pdf", clientSocket)
        elif (command == 5):
            response = clientSocket.recv(1024)
            msg  = response.decode()
            print(msg)
        elif (command == 6):
            running = False

        clientSocket.close()