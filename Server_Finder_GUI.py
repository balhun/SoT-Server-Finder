import webbrowser
import customtkinter as ctk
import threading
import subprocess
import requests
import psutil
import sys
import ctypes
from scapy.all import sniff, UDP, IP
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class SoTServerFinderGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sea of Thieves Server Finder")
        self.geometry("500x650")
        self.resizable(False, False)

        self.sot_id = ""
        self.sot_port = ""
        self.friend_ip = ""
        self.history = []
        self.current_server = ""

        self.iconbitmap(resource_path("Servants_of_the_Flame_icon.ico"))

        self.lbl_title = ctk.CTkLabel(self, text="SoT Server Finder", font=("Arial", 24, "bold"))
        self.lbl_title.pack(pady=(20, 10))

        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.pack(pady=10, padx=20, fill="x")
        
        self.lbl_friend = ctk.CTkLabel(self.frame_input, text="Friend's IP:Port (Optional):")
        self.lbl_friend.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.entry_friend = ctk.CTkEntry(self.frame_input, placeholder_text="e.g., 52.233.177.108:30437")
        self.entry_friend.pack(fill="x", padx=10, pady=(5, 10))

        self.frame_results = ctk.CTkFrame(self)
        self.frame_results.pack(pady=10, padx=20, fill="x")

        self.lbl_server_ip = ctk.CTkLabel(self.frame_results, text="", font=("Arial", 20, "underline"), cursor="hand2")
        self.lbl_server_ip.pack(pady=(15, 5))
        self.lbl_server_ip.bind("<Button-1>", self.open_ip_in_browser)

        self.lbl_location = ctk.CTkLabel(self.frame_results, text="", text_color="gray", font=("Arial", 16))
        self.lbl_location.pack(pady=5)

        self.lbl_status = ctk.CTkLabel(self.frame_results, text="Ready to Scan", font=("Arial", 16, "bold"), text_color="#3498db")
        self.lbl_status.pack(pady=(5, 15))

        self.lbl_log_title = ctk.CTkLabel(self, text="Session History:")
        self.lbl_log_title.pack(anchor="w", padx=25, pady=(10,0))
        
        self.textbox_log = ctk.CTkTextbox(self, height=180)
        self.textbox_log.pack(padx=20, pady=5, fill="both", expand=True)

        self.btn_scan = ctk.CTkButton(self, 
                                      text="Find Server", 
                                      height=50, 
                                      font=("Arial", 24, "bold"), 
                                      fg_color="#1f538d", 
                                      hover_color="#14375e",
                                      command=self.start_scan_thread)
        self.btn_scan.pack(side="bottom", fill="x", padx=20, pady=20)

    def log_msg(self, message):
        self.textbox_log.insert("0.0", message + "\n")

    def update_status(self, text, color="white"):
        self.lbl_status.configure(text=text, text_color=color)

    def find_sot_id(self):
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == "SoTGame.exe":
                return str(process.info['pid'])
        return None

    def get_sot_port_netstat(self, pid):
        sotPorts = []
        try:
            creation_flags = 0x08000000 if sys.platform == "win32" else 0
            
            activeConnections = subprocess.run(
                "netstat -anop udp", 
                stdout=subprocess.PIPE, 
                creationflags=creation_flags
            ).stdout.decode('utf-8', errors='ignore')
            
            connectionslist = activeConnections.splitlines()
            
            for i in connectionslist:
                if pid in i:
                    try:
                        port_part = i.split(":")[1].split(" ")[0]
                        port_int = int(port_part)
                        
                        if port_int != 3074:
                            sotPorts.append(port_int)
                    except:
                        continue
            if len(sotPorts) > 0:
                return sotPorts[0]
            else:
                return None
        except Exception as e:
            print(f"Netstat Error: {e}")
            return None

    def ip_lookup(self, ip_address):
        try:
            url = f"http://ip-api.com/json/{ip_address}"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "success":
                    return f"{data.get('country')}, {data.get('city')}"
        except:
            pass
        return "Unknown"

    def process_packet(self, packet):
        if UDP in packet and packet[UDP].dport == self.sot_port:
            return f"{packet[IP].src}:{packet[UDP].sport}"
        return None

    def start_scan_thread(self):
        self.btn_scan.configure(state="disabled", text="Scanning...")
        self.friend_ip = self.entry_friend.get().strip()
        
        thread = threading.Thread(target=self.run_scan_logic)
        thread.daemon = True
        thread.start()

    def run_scan_logic(self):
        pid = self.find_sot_id()
        if not pid:
            self.update_status("Error: SoTGame.exe not found! (Start the game)", "red")
            self.btn_scan.configure(state="normal", text="Find Server")
            return

        port = self.get_sot_port_netstat(pid)
        if not port:
            self.update_status("Error: No ports found! (Join a server)", "orange")
            self.btn_scan.configure(state="normal", text="Find Server")
            return
        
        self.sot_port = port
        self.update_status(f"Sniffing on Port {port}...", "#3498db")

        found_server_ip = None
        
        def internal_callback(pkt):
            nonlocal found_server_ip
            res = self.process_packet(pkt)
            if res:
                found_server_ip = res
                return True
        
        try:
            sniff(filter=f"udp port {port}", prn=internal_callback, count=10, timeout=5)
        except Exception as e:
            self.update_status(f"Sniff Error: {e}", "red")
            self.btn_scan.configure(state="normal", text="Find Server")
            return

        if found_server_ip:
            loc = self.ip_lookup(found_server_ip.split(":")[0])
            
            is_old = found_server_ip in self.history
            if not is_old:
                self.history.append(found_server_ip)

            is_friend = (found_server_ip == self.friend_ip)

            self.lbl_server_ip.configure(text=f"{found_server_ip}", text_color="#2ecc71" if is_friend else "#3498db")
            self.lbl_location.configure(text=f"Location: {loc}")
            
            log_msg = f"[{loc}] {found_server_ip}"
            
            if is_friend:
                self.update_status("MATCH FOUND! CONGRATULATIONS!", "#2ecc71")
                log_msg += " [FRIEND]"
            elif is_old:
                self.update_status("Server already visited.", "orange")
                log_msg += " [VISITED]"
            else:
                self.update_status("New Server Found", "#3498db")

            self.log_msg(log_msg)
        else:
            self.update_status("Scan Timeout. Couldn't find server!", "red")
        
        self.btn_scan.configure(state="normal", text="Find Server")

    def open_ip_in_browser(self, event):
        ip_text = self.lbl_server_ip.cget("text").strip()
        if ip_text:
            webbrowser.open(f"https://ip-api.com/#{self.lbl_server_ip.cget("text").split(":")[0]}")

if __name__ == "__main__":
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        print("CRITICAL: This tool must be run as Administrator. Or not. Who knows.")
    
    app = SoTServerFinderGUI()
    app.mainloop()