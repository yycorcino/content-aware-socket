import socket
import pickle
import subprocess
import platform

CLOSE_SOCKET_MSG = "!CLOSE_SOCKET!"

def getChoice():
    availableServices =  {  1: 'Retrieve Dental Records',
                            2: 'Retrieve Facebook Profile',
                            3: 'Retrieve Gaming Manual',
                            4: 'Retrieve Bank Statements',
                            5: 'Send an Emergency Call',
                            6: 'End Services'}

    print("Available Services: ")
    for index, service in availableServices.items():
        print(f"\t{index}: {service}")
    print("\n")

    while True:
        try:
            serviceOption = input("Please Select One Service From The Following Options (1-6): ")
            if (serviceOption.isdigit() and  int(serviceOption) in range(1, 7)):
                return serviceOption
            else:
                print("Invalid input. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def receivePdf(fileName, clientSocket):
    pdfData = b""
    while True:
        data = clientSocket.recv(1024)
        if not data:
            break
        pdfData += data

    with open(fileName, "wb") as pdf_file:
        pdf_file.write(pdfData)

    print(f"File Received and Saved to {fileName}")
    
    system_platform = platform.system()
    if (system_platform == "Darwin"):  
        subprocess.run(["open", fileName], check=True)
    elif (system_platform == "Windows"):
        subprocess.Popen(["start", fileName], shell=True)
    
if __name__ == "__main__":
    commandOptions = {1: 'EMILYANDERSON_DentalHistory_11-21-20',
                      2: 'facebookProfile',
                      3: 'CRAFTING_GUIDE',
                      4: 'DUSTINSTONE_BankStatement_3-9-16',
                      5: 'emergencySignal',
                      6: CLOSE_SOCKET_MSG}
    
    
    running = True
    while running: 
        command = int(getChoice())
        messageCommand = commandOptions[command]

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverAddress = ('172.16.33.137', 8080)
        clientSocket.connect(serverAddress)

        if (messageCommand == "emergencySignal"):
            additionalMsg = input("What is the Emergency: ")
            messageCommand = messageCommand + ": " + additionalMsg

        clientSocket.send(messageCommand.encode())

        if (command == 1):
            receivePdf("EMILYANDERSON_DentalHistory_11-21-20.pdf", clientSocket)
        elif (command == 3):
            receivePdf("CRAFTING_GUIDE.pdf", clientSocket)
        elif (command == 4):
            receivePdf("DUSTINSTONE_BankStatement_3-9-16.pdf", clientSocket)
        elif (command  == 2): 
            response = clientSocket.recv(1024)
            msg = pickle.loads(response)
            print(f"Here is your Facebook Data: {msg}")
        elif (command == 5):
            response = clientSocket.recv(1024)
            msg  = response.decode()
            print(msg)
        elif (command == 6):
            running = False
