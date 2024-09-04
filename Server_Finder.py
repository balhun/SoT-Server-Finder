import os
import subprocess
import psutil
from scapy.all import sniff, UDP, IP
import time
import sys

sotID = ""
sotPorts = []
captured_ip = []

def initialize():
    global sotID
    print("Welcome to Sea of Thieves Server Finder! (Version: Season 13)")
    start = input("Do you want to start searching? y/n\n")
    if start == "y":
        print()
        sotID = findSotID()
        if sotID == None:
            print("Sea of Thieves PID cannot be found! Aborting... (Maybe start the game)")
            time.sleep(5)
            clear = lambda: os.system('cls')
            clear()
            initialize()
        getSoTPort()
        sniffFoundPorts()
        restart = input("\nDo you want to try again? y/n\n")
        if restart == "y":
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
    sotID = findSotID()
    if sotID == None:
        print("Sea of Thieves PID cannot be found! Aborting... (Maybe start the game)")
        time.sleep(5)
        clear = lambda: os.system('cls')
        clear()
        initialize()
    getSoTPort()
    sniffFoundPorts()
    restart = input("\nDo you want to try again? y/n\n")
    if restart == "y":
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
    print(f"Searching for Sea of Thieves Ports...", end=" ")
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
        if (server_ip not in captured_ip):
            captured_ip.append(server_ip)
        
def sniffFoundPorts():
    print("Sniffing for Sea of Thieves Server IP...")
    sniff(filter=f"udp port {sotPorts[1]}", prn=process_packet, count=10, timeout=3)
    print(f"Found Sea of thieves server as: {captured_ip[0]}:{sotPorts[1]}")

initialize()