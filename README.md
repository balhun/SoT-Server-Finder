# Sea of Thieves Server Finder

A tool to help identify the IP address and port of incoming traffic for **Sea of Thieves**. This tool is compatible with both the retail and Insider versions of the game.

---

## ⚙️ Requirements

- [Npcap](https://npcap.com/)
  - During installation, **select "WinPcap compatibility mode"**.

## 🔧 Installation & Build

You can build the tool yourself using [PyInstaller](https://www.pyinstaller.org/):

```bash
pyinstaller your_script.py
```

## 🌐 How It Works

- This tool does **not** read, modify, or interact with game files.
- It also does **not** inject code or access the game's memory.
- It uses basic Windows CMD commands and functions to listen to internet traffic.
- Displays the **source IP and port** of incoming connections.

> Starting from **v4.0**, it uses [ip-api.com](https://ip-api.com) to identify the location (stamp) of the connecting player.

## 📝 Notes

- Make sure Npcap is installed correctly with WinPcap compatibility.
- Ensure you run the tool with sufficient permissions to capture network packets.

---

## 📢 Disclaimer

This tool is meant for informational and educational purposes only. It does not break the Sea of Thieves terms of service, as it does not interact with the game client, files, or memory.

Enjoy and sail safely!

