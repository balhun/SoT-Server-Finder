import os
import subprocess
import psutil
from scapy.all import sniff, UDP, IP
import time
import sys
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("Sea of Thieves Server Finder")
sotID = ""
sotPorts = []
captured_ip = []
captured_port = []

def initialize():
    global sotID
    print("Welcome to Sea of Thieves Server Finder!\nGuide:")
    print(" 1.) You and your friend have to start the game and join a server.")
    print(" 2.) Press Enter to search for the server's ip adress.")
    print(" 3.) Server hop until your ip adresses and ports are matching.")
    start = input("Do you want to start searching? Press Enter / Press any other key to exit\n")
    if start == "":
        print()
        sotPorts.clear()
        captured_ip.clear()
        captured_port.clear()
        sotID = findSotID()
        if sotID == None:
            print("Sea of Thieves PID cannot be found! Aborting... (Start the game)")
            time.sleep(5)
            clear = lambda: os.system('cls')
            clear()
            initialize()
        else:
            getSoTPort()
            sniffingSotIp()
        restart = input("   Do you want to try again?\n      Press Enter / Type any other key to exit\n")
        if restart == "":
            restarted()
        else:
            clear = lambda: os.system('cls')
            clear()
            initialize()
    else:
        sys.exit()

def restarted():
    print()
    global sotID
    sotPorts.clear()
    captured_ip.clear()
    captured_port.clear()
    sotID = findSotID()
    if sotID == None:
        print("Sea of Thieves PID cannot be found! Aborting... (Start the game)")
        time.sleep(5)
        clear = lambda: os.system('cls')
        clear()
        initialize()
    else:
        getSoTPort()
        sniffingSotIp()
    
def findSotID():
    processes = psutil.process_iter()
    for process in processes:
        if (process.name() == "SoTGame.exe"):
            sotID = str(process.pid)
            return sotID
        
def getSoTPort():
    try:  
        activeConnections = subprocess.run("netstat -anop udp", stdout=subprocess.PIPE).stdout.decode('utf-8')
        connectionslist = activeConnections.splitlines()
        for i in connectionslist:
            if sotID in i:
                sotPorts.append(int(i.split(":")[1].split(" ")[0]))
        sotPorts[1] #To throw an error
    except:
        print("Local ports cannot be found! Aborting... (Join a server)")
        time.sleep(5)
        clear = lambda: os.system('cls')
        clear()
        initialize()
        
        
def process_packet(packet):
    if UDP in packet and packet[UDP].dport == sotPorts[1]:
        server_ip = packet[IP].src
        server_port = packet[UDP].sport
        if (server_ip not in captured_ip):
            captured_ip.append(server_ip)
            captured_port.append(server_port)
        
def sniffingSotIp():
    try:
        sniff(filter=f"udp port {sotPorts[1]}", prn=process_packet, count=10, timeout=5)
        print(f"Found Sea of thieves server ip as: {captured_ip[0]}:{captured_port[0]}")
        
        restart = input("    Do you want to try again?\n      Press Enter / Press any other key to exit\n")
        if restart == "":
            restarted()
        else:
            clear = lambda: os.system('cls')
            clear()
            initialize()
    except:
        print("Server cannot be found! You probably left the game! Aborting...")
        time.sleep(5)
        clear = lambda: os.system('cls')
        clear()
        initialize()
        

initialize()