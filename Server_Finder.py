import os
import subprocess
import psutil
from scapy.all import sniff, UDP, IP
import time
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("Sea of Thieves Server Finder")
sotID = ""
sotPort = ""
friendIP = ""
sotIPPort = [""]

def findSotID():
    global sotID
    processes = psutil.process_iter()
    for process in processes:
        if (process.name() == "SoTGame.exe"):
            sotID = str(process.pid)
    if sotID == "":
        print("Sea of Thieves PID cannot be found! Aborting... (Start the game)")
        time.sleep(4)
        clear = lambda: os.system('cls')
        clear()
        initialize()
        
def getSoTPort():
    sotPorts = []
    global sotPort
    activeConnections = subprocess.run("netstat -anop udp", stdout=subprocess.PIPE).stdout.decode('utf-8')
    connectionslist = activeConnections.splitlines()
    for i in connectionslist:
        if sotID in i:
            sotPorts.append(int(i.split(":")[1].split(" ")[0]))
    try:
        sotPort = sotPorts[1]
    except:
        print("Local ports cannot be found! Aborting... (Join a server)")
        sotPort = ""
        time.sleep(4)
        clear = lambda: os.system('cls')
        clear()
        initialize()

def process_packet(packet):
    global sotIPPort
    if UDP in packet and packet[UDP].dport == sotPort:
        message = f"{packet[IP].src}:{packet[UDP].sport}"
        if sotIPPort[-1] != message:
            sotIPPort.append(message)

def sniff_packets():
    global sotIPPort
    try:
        getSoTPort()
        if sotPort != "":
            sniff(filter=f"udp port {sotPort}", prn=process_packet, count=10, timeout=5)
            print("Found Sea of Thieves server ip as: " + sotIPPort[-1])
            
            if sotIPPort[-1] == friendIP:
                print("You are on your friend's server!          Congratulations!")
            else:
                print(f"Your are NOT on your friend's server :(")
                
            if sotIPPort[-1] in sotIPPort[:-1]:
                print("You already been on this server. :(")
            else:
                print("You haven't been on this server yet!")
    except:
        print("Something went wrong with finding the IP")
        print("Going back to the menu!")
        time.sleep(4)
        clear = lambda: os.system('cls')
        clear()
        initialize()

def user_input():
    command = input("\nPress Enter to search / Press any other key to exit\n")
    if command.lower() == "":
        findSotID()
        sniff_packets()
        user_input()
    else:
        print("Going back to the menu!")
        time.sleep(4)
        clear = lambda: os.system('cls')
        clear()
        initialize()

def initialize():
    global friendIP
    print("Welcome to Sea of Thieves Server Finder!\nGuide:")
    print(" 1.) You and your friend have to start the game and join a server.")
    print(" 2.) Press Enter to search for the server's ip adress.")
    print(" 3.) Server hop until your ip adresses and ports are matching.\n")

    friendIP = input("  Type in your friend's ip and port: e.g.: 52.233.177.108:30437\n  (Otherwise you can leave this empty)\n")
    user_input()
    
initialize()