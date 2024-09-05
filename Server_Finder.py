import os
import subprocess
import psutil
from scapy.all import sniff, UDP, IP
import time
import sys

sotID = ""
sotPorts = []
captured_ip = []
captured_port = []

def initialize():
    global sotID
    print("Welcome to Sea of Thieves Server Finder!\nGuide:")
    print(" 1.) You and your friend have to start the game and join a server.")
    print(" 2.) Type \"y\" and search for ip adress.")
    print(" 3.) Check if you have matching ip adresses with your friend.")
    print(" 4.) If you don't, server hop to another server in game, and search for your ip again.")
    print("     If you have matching ip adresses, you're good to go!\n")
    start = input("Do you want to start searching? Y / N or any other key (exit)\n")
    if start == "Y" or start == "y":
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
        getSoTPort()
        sniffFoundPorts()
        restart = input("    Do you want to try again? Y / N\n")
        if restart == "Y" or restart == "y":
            restarted()
        else:
            clear = lambda: os.system('cls')
            clear()
            initialize()
    else:
        sys.exit()

def restarted():
    global sotID
    print("\n")
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
    getSoTPort()
    sniffFoundPorts()
    restart = input("    Do you want to try again? Y / N\n")
    if restart == "Y" or restart == "y":
            restarted()
    else:
        clear = lambda: os.system('cls')
        clear()
        initialize()

def findSotID():
    print(f"Searching for Sea of Thieves PID...", end=" ")
    processes = psutil.process_iter()
    for process in processes:
        if (process.name() == "SoTGame.exe"):
            sotID = str(process.pid)
            print(f"Found! ({sotID})")
            return sotID
        
def getSoTPort():
    print(f"Searching for local Sea of Thieves Port...", end=" ")
    sotPorts.clear()
    try:  
        activeConnections = subprocess.run("netstat -anop udp", stdout=subprocess.PIPE).stdout.decode('utf-8')
        activeConnections.strip()
        connectionslist = activeConnections.splitlines()
        for i in connectionslist:
            if sotID in i:
                sotPorts.append(int(i.split(":")[1].split(" ")[0]))
        print(f"Found! ({sotPorts[1]})")
    except:
        print("Ports cannot be found! Aborting... (Join a server)")
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
        
def sniffFoundPorts():
    print("Sniffing for Sea of Thieves Server IP...")
    sniff(filter=f"udp port {sotPorts[1]}", prn=process_packet, count=10, timeout=20)
    print(f"\nFound Sea of thieves server ip as: {captured_ip[0]}:{captured_port[0]}")
    
initialize()