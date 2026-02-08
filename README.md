# Sea of Thieves Server Finder

A tool to help identify the IP address and port of incoming traffic for **Sea of Thieves**. This tool is compatible with both the retail and Insider versions of the game.

---

## Requirements

- This tool requires [Npcap](https://npcap.com/) to function.

> During installation, **select "WinPcap compatibility mode"**.

## Installation & Build

You can build the tool yourself using [PyInstaller](https://www.pyinstaller.org/):

```bash
pyinstaller --noconsole --onefile --icon="Servants_of_the_Flame_icon.ico" Server_Finder.py
```
```bash
pyinstaller --noconsole --onefile --icon="Servants_of_the_Flame_icon.ico" --add-data "Servants_of_the_Flame_icon.ico;." Server_Finder_GUI.py
```

---

## How It Works
1. The program identifies the active Sea of Thieves process and scans your network connections to pinpoint the specific UDP port the game is using to communicate.
2. It then analyzes network traffic on that port to capture the game server's IP address and port number directly from the data packets.
3. Finally, it cross-references the server IP with a geolocation API and displays the server's region, city, IP and Port, allowing you to confirm if you are in the same lobby as your friends.
> Starting from **v4.0**, it uses [ip-api.com](https://ip-api.com) to identify the location (stamp) of the connecting player.

---

## Important
- Make sure Npcap is installed correctly with WinPcap compatibility.
- Ensure you run the tool with sufficient permissions to capture network packets.

---

## Disclaimer
- This tool does **not** read, modify, or interact with game files.
- It also does **not** inject code or access the game's memory.
- It uses basic Windows CMD commands and functions to listen to internet traffic.
- Displays the **source IP and port** of the Microsoft Datacenter *(Sea of Thieves Server)* you're connected to.

In conclusion, this program is for informational and educational purposes only. It does not break the Sea of Thieves terms of service, as it does not interact with the game client, files, or memory.

Enjoy and sail safely!
