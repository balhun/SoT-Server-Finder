import os
import subprocess
import psutil
from scapy.all import sniff, UDP, IP
import time
import sys
import ctypes
import requests
import msvcrt

ctypes.windll.kernel32.SetConsoleTitleW("Sea of Thieves Server Finder")
sotID = ""
sotPort = ""
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
        if sotID in i and int(i.split(":")[1].split(" ")[0]) != 3074:
            sotPorts.append(int(i.split(":")[1].split(" ")[0]))
    try:
        sotPort = sotPorts[0]
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
            print("Found Sea of Thieves server ip as:\n\t- " + sotIPPort[-1])
                
            if sotIPPort[-1] in sotIPPort[:-1]:
                print("- You already been on this server. :(")
            
            lookup = (ip_lookup(sotIPPort[-1].split(":")[0]))
            if "Country" in lookup and "City" in lookup:
                print(f"Your stamp is:\n - {lookup["Country"]}, {lookup["City"]}")
            else:
                print("API error, couldn't get stamp location.")

        time.sleep(2)
        while msvcrt.kbhit():
            msvcrt.getch()
        
    except:
        print("Something went wrong with finding the IP")
        print("Going back to the menu!")
        time.sleep(3)
        clear = lambda: os.system('cls')
        clear()
        initialize()

def ip_lookup(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return {
                "Country": data.get("country"),
                "City": data.get("city"),
            }
        else:
            return {"Error": data.get("message", "Unknown error")}
    else:
        return {"Error": "Failed to connect to IP-API"}

def user_input():
    print("\nPress Enter to search / Press any other key to exit\n")
    key = msvcrt.getch()
    if key == b'\x1b':  # ESC key
        print("Going back to the menu!")
        time.sleep(4)
        clear = lambda: os.system('cls')
        clear()
        initialize()
    elif key == b'\r':
        findSotID()
        sniff_packets()
        user_input()

def initialize():
    print("Welcome to Sea of Thieves Server Finder!\nGuide:")
    print(" 1.) You and your friend have to start the game and join a server.")
    print(" 2.) Press Enter to search for the server's ip adress.")
    print(" 3.) Server hop until your ip adresses and ports are matching.\n")
    user_input()
    
initialize()